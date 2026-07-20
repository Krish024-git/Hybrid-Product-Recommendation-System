import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from recommender import HybridRecommender

def main():
    print("==================================================")
    print("   Starting Recommendation System Model Training   ")
    print("==================================================")
    
    # Initialize recommender
    recommender = HybridRecommender()
    
    # Load raw data from database
    print("Loading data from database...")
    recommender.load_data_from_db()
    
    if recommender.products_df is None or len(recommender.products_df) == 0:
        print("Error: Products table in database is empty. Please run db_setup.py first!")
        return
        
    print(f"Loaded {len(recommender.products_df)} products and {len(recommender.ratings_df)} rating records.")
    
    # Train content-based filtering
    print("\nTraining Content-Based Filter (TF-IDF & Cosine Similarity matrix)...")
    recommender.train_content_based()
    print("Content-based model training complete.")
    
    # Train collaborative filtering (SVD)
    print("\nTraining Collaborative Filter (SVD Matrix Factorization)...")
    recommender.train_collaborative()
    print("Collaborative model training complete.")
    
    # Save the models
    print("\nSaving trained models to disk...")
    recommender.save_models()
    print("==================================================")
    print("   Model Training Process Finished Successfully   ")
    print("==================================================")

if __name__ == "__main__":
    main()
