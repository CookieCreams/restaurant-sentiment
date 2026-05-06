import os
os.environ["HF_HOME"] = "./models"
os.environ["HF_HUB_CACHE"] = "./models/hub"
os.environ["TRANSFORMERS_CACHE"] = "./models"

from fastapi import FastAPI
from pydantic import BaseModel
import duckdb
import sys
sys.path.append(".")
from model.predict import predict_sentiment

app = FastAPI(title="Restaurant Sentiment API")

db_path = "reviews.db"
read_only = os.path.exists(db_path)
conn = duckdb.connect(db_path, read_only=read_only)

# --- Schéma de requête ---
class ReviewRequest(BaseModel):
    text: str

# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "Restaurant Sentiment API 🍕"}

@app.post("/predict")
def predict(req: ReviewRequest):
    """Analyse le sentiment d'un texte"""
    return predict_sentiment(req.text)

@app.get("/stats")
def stats():
    """Statistiques globales de la base"""
    return {
        "distribution": conn.execute("""
            SELECT sentiment, COUNT(*) as nb
            FROM reviews WHERE sentiment IS NOT NULL
            GROUP BY sentiment ORDER BY nb DESC
        """).df().to_dict(orient="records"),

        "par_note": conn.execute("""
            SELECT stars, ROUND(AVG(sentiment_score), 3) as score_moyen
            FROM reviews WHERE sentiment IS NOT NULL
            GROUP BY stars ORDER BY stars
        """).df().to_dict(orient="records"),

        "par_langue": conn.execute("""
            SELECT langue, COUNT(*) as nb
            FROM reviews WHERE langue IS NOT NULL
            GROUP BY langue ORDER BY nb DESC
            LIMIT 10
        """).df().to_dict(orient="records")
    }

@app.get("/reviews")
def get_reviews(sentiment: str = None, limit: int = 20):
    """Récupère des avis filtrés par sentiment"""
    where = f"WHERE sentiment = '{sentiment}'" if sentiment else "WHERE sentiment IS NOT NULL"
    df = conn.execute(f"""
        SELECT review_id, stars, sentiment, sentiment_score, text, date
        FROM reviews {where}
        ORDER BY RANDOM()
        LIMIT {limit}
    """).df()
    return df.to_dict(orient="records")