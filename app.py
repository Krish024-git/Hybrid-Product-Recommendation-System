import os
import sys
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

# Add 'src' directory to Python path to import our modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from recommender import HybridRecommender

app = Flask(__name__)
app.secret_key = "aurora_secret_key_recommendations_system"

# Global Recommender Instance
recommender = HybridRecommender()
recommender.load_models()

def get_current_user():
    """Extracts active simulated user ID from request parameters or session."""
    # Check if user passed query param to switch simulated profile
    sim_user_param = request.args.get("sim_user")
    if sim_user_param:
        try:
            user_id = int(sim_user_param)
            session["sim_user"] = user_id
            return user_id
        except ValueError:
            pass
            
    # Fallback to session, then default to user 1
    if "sim_user" not in session:
        session["sim_user"] = 1
    return session["sim_user"]

@app.route("/")
def home():
    current_user = get_current_user()
    
    # Extract alpha parameter for model fine-tuning (default to 0.5)
    alpha_param = request.args.get("alpha")
    alpha = 0.5
    if alpha_param:
        try:
            alpha = float(alpha_param)
        except ValueError:
            pass
            
    # Reload data from DB in case ratings/history changed
    recommender.load_data_from_db()
    
    # 1. Get List of all products
    products = recommender.products_df.to_dict(orient="records")
    
    # Get categories and brands for filter menus
    categories = sorted(recommender.products_df["category"].unique().tolist())
    brands = sorted(recommender.products_df["brand"].unique().tolist())
    
    # 2. Get Hybrid Recommendations (Top 5) with fine-tuned alpha
    hybrid_recs_df = recommender.get_hybrid_recommendations(user_id=current_user, top_n=5, alpha=alpha)
    
    recommendations = []
    if hybrid_recs_df is not None and not hybrid_recs_df.empty:
        recommendations = hybrid_recs_df.to_dict(orient="records")
        
    return render_template(
        "home.html",
        products=products,
        recommendations=recommendations,
        categories=categories,
        brands=brands,
        current_user=current_user,
        alpha=alpha
    )

@app.route("/product/<product_id>")
def product_details(product_id):
    current_user = get_current_user()
    
    # Find product by ID
    matching_products = recommender.products_df[recommender.products_df["product_id"] == product_id]
    if matching_products.empty:
        return redirect(url_for("page_not_found"))
        
    product = matching_products.iloc[0].to_dict()
    
    # Get similar items (Content-Based, Top 5)
    similar_df = recommender.get_similar_products(product_id=product_id, top_n=5)
    similar_products = []
    if similar_df is not None and not similar_df.empty:
        similar_products = similar_df.to_dict(orient="records")
        
    # Log this viewing interaction into DB history logs
    recommender.log_recommendation(
        user_id=current_user,
        product_id=product_id,
        recommendation_type="Manual View"
    )
        
    return render_template(
        "product.html",
        product=product,
        similar_products=similar_products,
        current_user=current_user
    )

@app.route("/log_recommendation/<product_id>/<rec_type>")
def log_recommendation_to_db(product_id, rec_type):
    current_user = get_current_user()
    recommender.log_recommendation(
        user_id=current_user,
        product_id=product_id,
        recommendation_type=rec_type
    )
    # Redirect to details page
    return redirect(url_for("product_details", product_id=product_id))

@app.route("/history")
def history():
    current_user = get_current_user()
    
    # Retrieve logged logs
    history_df = recommender.get_recommendation_history(user_id=current_user, limit=15)
    
    return render_template(
        "history.html",
        history_df=history_df,
        current_user=current_user
    )

@app.route("/clear_history")
def clear_history_to_db():
    current_user = get_current_user()
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "recommendation_system.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recommendation_history WHERE user_id = ?", (current_user,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error clearing history logs: {e}")
        
    return redirect(url_for("history", sim_user=current_user))

@app.route("/about")
def about():
    current_user = get_current_user()
    return render_template("about.html", current_user=current_user)

@app.route("/contact")
def contact():
    current_user = get_current_user()
    return render_template("contact.html", current_user=current_user)

# Beautiful 404 Error handler Page
@app.errorhandler(404)
def page_not_found(e):
    current_user = get_current_user()
    return render_template("404.html", current_user=current_user), 404

if __name__ == "__main__":
    # Load config and start local debug server
    app.run(debug=True, port=5000)
