import os
import sqlite3
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "recommendation_system.db")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Custom SVD Implementation as a highly robust fallback
class CustomSVD:
    """
    A lightweight, pure-NumPy Singular Value Decomposition (SVD) matrix factorization 
    recommender. Replicates surprise's SVD using Stochastic Gradient Descent (SGD).
    """
    def __init__(self, n_factors=20, lr=0.005, reg=0.02, epochs=20):
        self.n_factors = n_factors
        self.lr = lr
        self.reg = reg
        self.epochs = epochs
        self.global_mean = 3.0
        self.u_map = {}
        self.i_map = {}
        self.P = None
        self.Q = None
        self.bu = None
        self.bi = None

    def fit(self, df_ratings):
        self.global_mean = df_ratings['rating'].mean()
        users = sorted(df_ratings['user_id'].unique())
        items = sorted(df_ratings['product_id'].unique())
        
        self.u_map = {u: idx for idx, u in enumerate(users)}
        self.i_map = {i: idx for idx, i in enumerate(items)}
        
        n_users = len(users)
        n_items = len(items)
        
        # Initialize latent matrices and biases
        self.P = np.random.normal(0, 0.1, (n_users, self.n_factors))
        self.Q = np.random.normal(0, 0.1, (n_items, self.n_factors))
        self.bu = np.zeros(n_users)
        self.bi = np.zeros(n_items)
        
        # Run SGD
        for epoch in range(self.epochs):
            # Shuffle ratings for SGD
            df_shuffled = df_ratings.sample(frac=1.0).reset_index(drop=True)
            for _, row in df_shuffled.iterrows():
                u_id = row['user_id']
                i_id = row['product_id']
                r = row['rating']
                
                # Get matrix index
                u = self.u_map[u_id]
                i = self.i_map[i_id]
                
                # Prediction
                pred = self.global_mean + self.bu[u] + self.bi[i] + np.dot(self.P[u], self.Q[i])
                err = r - pred
                
                # Update biases
                self.bu[u] += self.lr * (err - self.reg * self.bu[u])
                self.bi[i] += self.lr * (err - self.reg * self.bi[i])
                
                # Update user/item vectors
                p_temp = self.P[u].copy()
                self.P[u] += self.lr * (err * self.Q[i] - self.reg * self.P[u])
                self.Q[i] += self.lr * (err * p_temp - self.reg * self.Q[i])

    def predict(self, user_id, product_id):
        u_seen = user_id in self.u_map
        i_seen = product_id in self.i_map
        
        u_idx = self.u_map[user_id] if u_seen else None
        i_idx = self.i_map[product_id] if i_seen else None
        
        u_bias = self.bu[u_idx] if u_seen else 0.0
        i_bias = self.bi[i_idx] if i_seen else 0.0
        dot_product = np.dot(self.P[u_idx], self.Q[i_idx]) if (u_seen and i_seen) else 0.0
        
        est = self.global_mean + u_bias + i_bias + dot_product
        # Clip score between [1.0, 5.0]
        return float(np.clip(est, 1.0, 5.0))

class HybridRecommender:
    """
    Combines Content-Based Filtering (TF-IDF & Cosine Similarity) 
    and Collaborative Filtering (SVD) for personalized product recommendations.
    """
    def __init__(self):
        self.products_df = None
        self.ratings_df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.svd_model = None
        self.is_surprise_model = False
        
    def load_data_from_db(self):
        """Loads products and ratings from SQLite DB."""
        conn = sqlite3.connect(DB_PATH)
        self.products_df = pd.read_sql_query("SELECT * FROM products", conn)
        self.ratings_df = pd.read_sql_query("SELECT * FROM ratings", conn)
        conn.close()
        
    def train_content_based(self):
        """Fits TF-IDF vectorizer and calculates Cosine Similarity."""
        if self.products_df is None:
            self.load_data_from_db()
            
        # Combine relevant metadata fields into a single text representation
        self.products_df['metadata_soup'] = (
            self.products_df['product_name'] + " " +
            self.products_df['brand'] + " " +
            self.products_df['category'] + " " +
            self.products_df['description']
        )
        
        # Fit TF-IDF Vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.products_df['metadata_soup'])
        
        # Calculate Cosine Similarity matrix
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
    def save_models(self):
        """Saves content-based variables and collaborative filter to disk."""
        # Save content-based artifacts
        joblib.dump(self.tfidf_vectorizer, os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"))
        joblib.dump(self.tfidf_matrix, os.path.join(MODELS_DIR, "tfidf_matrix.pkl"))
        joblib.dump(self.cosine_sim, os.path.join(MODELS_DIR, "cosine_sim.pkl"))
        
        # Save SVD model
        joblib.dump(self.svd_model, os.path.join(MODELS_DIR, "svd_model.pkl"))
        joblib.dump(self.is_surprise_model, os.path.join(MODELS_DIR, "is_surprise_model.pkl"))
        print("Models successfully saved to models/ directory.")

    def load_models(self):
        """Loads trained models from models/ directory. Falls back to training if not found."""
        try:
            self.tfidf_vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"))
            self.tfidf_matrix = joblib.load(os.path.join(MODELS_DIR, "tfidf_matrix.pkl"))
            self.cosine_sim = joblib.load(os.path.join(MODELS_DIR, "cosine_sim.pkl"))
            self.svd_model = joblib.load(os.path.join(MODELS_DIR, "svd_model.pkl"))
            self.is_surprise_model = joblib.load(os.path.join(MODELS_DIR, "is_surprise_model.pkl"))
            self.load_data_from_db()
            print("Models successfully loaded from disk.")
        except Exception as e:
            print(f"Warning: Could not load cached models ({e}). Re-training models...")
            self.load_data_from_db()
            self.train_content_based()
            self.train_collaborative()
            self.save_models()

    def train_collaborative(self):
        """Fits SVD collaborative filter. Prefers Surprise SVD, falls back to CustomSVD."""
        if self.ratings_df is None:
            self.load_data_from_db()
            
        try:
            from surprise import Dataset, Reader, SVD
            print("Attempting to train SVD using Surprise library...")
            reader = Reader(rating_scale=(1, 5))
            # Load from pandas
            data = Dataset.load_from_df(self.ratings_df[['user_id', 'product_id', 'rating']], reader)
            trainset = data.build_full_trainset()
            
            model = SVD(n_factors=20, lr_all=0.005, reg_all=0.02, n_epochs=20)
            model.fit(trainset)
            
            self.svd_model = model
            self.is_surprise_model = True
            print("Successfully trained SVD model via Surprise.")
        except Exception as e:
            print(f"Surprise Library SVD training failed or not available ({e}). Using CustomSVD fallback...")
            model = CustomSVD(n_factors=20, lr=0.005, reg=0.02, epochs=20)
            model.fit(self.ratings_df)
            
            self.svd_model = model
            self.is_surprise_model = False
            print("Successfully trained custom SVD fallback model.")

    def get_svd_prediction(self, user_id, product_id):
        """Helper to compute SVD rating prediction regardless of library used."""
        if self.is_surprise_model:
            # Surprise predict returns a prediction object, .est holds the rating
            return float(self.svd_model.predict(uid=user_id, iid=product_id).est)
        else:
            return float(self.svd_model.predict(user_id, product_id))

    # --- Feature 1: Similar Products (Content-Based) ---
    def get_similar_products(self, product_id, top_n=5):
        """Returns the top_n most content-similar products for a product_id."""
        if self.products_df is None or self.cosine_sim is None:
            self.load_models()
            
        # Get index of the product
        idx_list = self.products_df[self.products_df['product_id'] == product_id].index
        if len(idx_list) == 0:
            return pd.DataFrame()  # Product not found
        idx = idx_list[0]
        
        # Get pairwise similarity scores of all products with this product
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort products by similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get scores of the top_n most similar products (skipping the input product itself)
        top_sim_scores = [score for score in sim_scores if score[0] != idx][:top_n]
        
        similar_indices = [score[0] for score in top_sim_scores]
        similar_scores = [score[1] for score in top_sim_scores]
        
        similar_products = self.products_df.iloc[similar_indices].copy()
        similar_products['similarity_score'] = similar_scores
        
        return similar_products

    # --- Feature 2: Personalized Collaborative Recommendations ---
    def get_collaborative_recommendations(self, user_id, top_n=5):
        """Recommends products by collaborative filtering rating predictions."""
        if self.products_df is None or self.svd_model is None:
            self.load_models()
            
        # Get list of products rated by this user to exclude them from main recommendation list
        user_ratings = self.ratings_df[self.ratings_df['user_id'] == user_id]
        rated_product_ids = set(user_ratings['product_id'].tolist())
        
        unrated_products = self.products_df[~self.products_df['product_id'].isin(rated_product_ids)].copy()
        
        predictions = []
        for pid in unrated_products['product_id']:
            pred_rating = self.get_svd_prediction(user_id, pid)
            predictions.append(pred_rating)
            
        unrated_products['predicted_rating'] = predictions
        
        # Sort products by predicted rating
        recommended_products = unrated_products.sort_values(by='predicted_rating', ascending=False).head(top_n)
        return recommended_products

    # --- Feature 3: Hybrid Recommendation System ---
    def get_hybrid_recommendations(self, user_id, top_n=5, alpha=0.5):
        """
        Combines content-based user preference profile score and 
        collaborative SVD predicted rating score to recommend products.
        """
        if self.products_df is None or self.svd_model is None or self.cosine_sim is None:
            self.load_models()
            
        # Get list of products rated by this user to exclude them
        user_ratings = self.ratings_df[self.ratings_df['user_id'] == user_id]
        rated_product_ids = set(user_ratings['product_id'].tolist())
        
        # Calculate content preferences for the user
        # User preference vector = weighted sum of content representations of highly rated products
        positive_ratings = user_ratings[user_ratings['rating'] >= 3.5]
        
        # If the user has no high ratings, fall back to pure collaborative SVD
        if len(positive_ratings) == 0:
            # Cold-start or new user scenario with few interactions: return collaborative recommendations
            collaborative_recs = self.get_collaborative_recommendations(user_id, top_n=top_n)
            collaborative_recs['hybrid_score'] = collaborative_recs['predicted_rating'] / 5.0
            return collaborative_recs
            
        # Compute user's average content similarity profile across all products
        # Get indices of positive products in the main dataframe
        liked_indices = self.products_df[self.products_df['product_id'].isin(positive_ratings['product_id'])].index.tolist()
        
        # Mean similarity score of all products relative to products this user liked
        content_scores = np.mean(self.cosine_sim[liked_indices], axis=0)
        
        # Normalize content score to [0, 1]
        max_c = content_scores.max()
        min_c = content_scores.min()
        if max_c != min_c:
            content_scores = (content_scores - min_c) / (max_c - min_c)
        else:
            content_scores = np.ones_like(content_scores)
            
        recommendations = []
        for idx, row in self.products_df.iterrows():
            pid = row['product_id']
            
            # Exclude already rated items
            if pid in rated_product_ids:
                continue
                
            # Collaborative rating prediction
            svd_pred = self.get_svd_prediction(user_id, pid)
            # Normalize collaborative score (1 to 5 stars -> 0 to 1)
            norm_svd_score = (svd_pred - 1.0) / 4.0
            
            # Content score for this item
            content_score = content_scores[idx]
            
            # Hybrid weighted combination
            hybrid_score = (alpha * content_score) + ((1 - alpha) * norm_svd_score)
            
            recommendations.append({
                "product_id": pid,
                "product_name": row['product_name'],
                "brand": row['brand'],
                "category": row['category'],
                "price": row['price'],
                "rating": row['rating'],
                "image_path": row['image_path'],
                "description": row['description'],
                "predicted_rating": svd_pred,
                "content_score": content_score,
                "hybrid_score": hybrid_score
            })
            
        df_recs = pd.DataFrame(recommendations)
        if df_recs.empty:
            return df_recs
            
        # Return top N items sorted by hybrid score
        return df_recs.sort_values(by='hybrid_score', ascending=False).head(top_n)

    # --- Feature 4: Recommendation History Logging ---
    def log_recommendation(self, user_id, product_id, recommendation_type):
        """Logs a recommended item in SQLite to record user recommendation history."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO recommendation_history (user_id, product_id, recommendation_type) VALUES (?, ?, ?)",
                (user_id, product_id, recommendation_type)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error logging recommendation history: {e}")

    def get_recommendation_history(self, user_id, limit=10):
        """Retrieves user's recommendation history logs joined with product details."""
        try:
            conn = sqlite3.connect(DB_PATH)
            query = """
                SELECT h.history_id, h.timestamp, h.recommendation_type, p.product_id, 
                       p.product_name, p.brand, p.category, p.price, p.rating, p.image_path
                FROM recommendation_history h
                JOIN products p ON h.product_id = p.product_id
                WHERE h.user_id = ?
                ORDER BY h.timestamp DESC
                LIMIT ?
            """
            df_history = pd.read_sql_query(query, conn, params=(user_id, limit))
            conn.close()
            return df_history
        except Exception as e:
            print(f"Error getting history: {e}")
            return pd.DataFrame()
