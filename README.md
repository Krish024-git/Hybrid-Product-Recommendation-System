# Hybrid Product Recommendation System

A production-ready, feature-rich **Hybrid Product Recommendation System** built using Python, Flask, SQLite, and Scikit-learn. This project demonstrates how content-based filtering (TF-IDF + Cosine Similarity) and collaborative filtering (Singular Value Decomposition via Matrix Factorization) can be combined mathematically to build a personalized web commerce experience.

---

## 🌟 Features

1. **AI-Powered Recommendation Engines**:
   - **Content-Based Filtering**: Recommends items similar to the active product using TF-IDF analysis on names, brands, categories, and descriptions combined with Cosine Similarity metrics.
   - **Collaborative Filtering (SVD)**: Predicts user-item ratings by identifying latent preferences using Singular Value Decomposition.
   - **Hybrid System**: Standardizes and blends both similarity scores ($\alpha \times \text{Content} + (1-\alpha) \times \text{Collaborative}$) to generate rankings.
2. **Interactive Simulated Profiles**:
   - Navbar profile-switching allows simulated browsing as different User IDs (User #1 to User #20) to observe collaborative rating shifts immediately.
3. **Advanced Store Catalog UI**:
   - Live search matching, category filtering, brand tags, price sliders, and rating range queries powered by lightweight client-side JavaScript.
4. **Rich Analytics Dashboard**:
   - Embeds exploratory visualizations (rating volumes, user activity distribution, category densities, brand counts, and item popularities) rendered during the training run.
5. **Interactive Jupyter Notebook**:
   - A step-by-step educational notebook (`Product_Recommendation_System.ipynb`) detailing data cleaning, mathematical equations, matrix calculations, SVD training, and metrics evaluation.
6. **Interaction History Tracking**:
   - Saves views and recommendation clicks inside local SQLite database history logs.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib
- **Database**: SQLite3
- **Visualization**: Matplotlib, Seaborn
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (via CDN), Custom glassmorphism CSS
- **Notebook**: Jupyter

---

## 📂 Project Structure

```text
Product Recommendation/
├── data/
│   ├── products.csv               # Synthetic Amazon products catalog
│   ├── users.csv                  # Demographics user profiles
│   ├── ratings.csv                # User ratings interaction matrix
│   └── recommendation_system.db   # SQLite Database storing all relational tables
├── models/
│   ├── tfidf_vectorizer.pkl       # Saved TF-IDF fitted vectorizer
│   ├── tfidf_matrix.pkl           # Saved document tf-idf matrix representation
│   ├── cosine_sim.pkl             # Cached pairwise cosine similarity matrix
│   ├── svd_model.pkl              # Saved SVD model weights (user/item matrices & biases)
│   └── is_surprise_model.pkl      # Flag denoting model type used (Surprise vs Custom Fallback)
├── static/
│   ├── css/
│   │   └── style.css              # Custom styling (glassmorphism, blobs, canvas background rules)
│   ├── js/
│   │   └── app.js                 # Local search engine, range sliders, canvas particles loop
│   └── images/
│       ├── products/              # Locally generated vector SVGs representing products
│       └── visualizations/        # Graph plots (PNGs) loaded in the analytics dashboard
├── templates/
│   ├── base.html                  # Base structure containing navbar, footer, background layers
│   ├── home.html                  # Home storefront, sliders, filters, hybrid cards carousel
│   ├── product.html               # Item details page and similar content recommended listings
│   ├── history.html               # Logged interaction logs history
│   ├── about.html                 # Analytics dashboard demonstrating EDA charts
│   ├── contact.html               # Contact feedback form
│   └── 404.html                   # Customized 404 latent space error page
├── src/
│   ├── data_generator.py          # Builds mock datasets & generates SVG image catalog
│   ├── db_setup.py                # Initializes SQLite tables & ingests generated CSV files
│   ├── recommender.py             # Defines HybridRecommender class and Custom SVD class
│   └── train.py                   # Script fitting SVD + TF-IDF models and dumping weights
├── Product_Recommendation_System.ipynb # Full educational analysis notebook
├── requirements.txt               # Required package list
└── README.md                      # Documentation
```

---

## ⚙️ Installation & Setup

1. **Clone or Navigate to the Directory**:
   ```bash
   cd "Product Recommendation"
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Datasets & Products Images**:
   ```bash
   python src/data_generator.py
   ```
   *This populates the `data/` directory with `products.csv`, `users.csv`, and `ratings.csv`, and builds the SVG vector images directory.*

4. **Initialize SQLite Database**:
   ```bash
   python src/db_setup.py
   ```
   *Ingests the CSV files and builds the table schemas inside `data/recommendation_system.db`.*

5. **Train the Models**:
   ```bash
   python src/train.py
   ```
   *Fits the custom Singular Value Decomposition matrix model and the TF-IDF cosine spaces, caching weights in `models/`.*

---

## 🚀 Running the Web Application

1. **Start the Flask Server**:
   ```bash
   python app.py
   ```
2. **Access in the Browser**:
   Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser.

3. **Simulating Collaborative Matrix Filtering**:
   - Go to the top-right navbar dropdown and choose a different user profile (e.g., User #3, User #7).
   - Observe how the **Recommended For You** carousel updates immediately, presenting products tailored specifically to the latent category preferences associated with that user profile.

---

## 📘 Running the Jupyter Notebook

To explore the mathematical walk-through and visual EDA:
```bash
jupyter notebook Product_Recommendation_System.ipynb
```
*You can execute all cells from top to bottom. It will recalculate evaluation scores (RMSE & MAE) and update the PNG charts in `static/images/visualizations/`.*

---

## 🔮 Future Scope

1. **Deep Learning Collaborative Filtering**:
   - Implementing neural collaborative filtering (NCF) using PyTorch or TensorFlow to learn non-linear latent embeddings.
2. **Real-time Streaming Matrix Updates**:
   - Integrating Redis to capture mouse movements, click behaviors, and view counts to update user preference vectors dynamically without retraining.
3. **Session-based Recommendations**:
   - Using recurrent GRU networks to predict purchase intents within anonymous sessions without user accounts.

---

## 📄 License & Credits

Designed and coded by **Aurora Recommender Systems Team**. Open-sourced under the MIT License.
