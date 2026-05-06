import os
os.environ["HF_HOME"] = "./models"
os.environ["HF_HUB_CACHE"] = "./models/hub"
os.environ["TRANSFORMERS_CACHE"] = "./models"

import duckdb
import pandas as pd
from model.predict import predict_sentiment
from tqdm import tqdm

conn = duckdb.connect("reviews.db")

# Ajoute les colonnes si elles n'existent pas
conn.execute("""
    ALTER TABLE reviews ADD COLUMN IF NOT EXISTS langue VARCHAR;
    ALTER TABLE reviews ADD COLUMN IF NOT EXISTS sentiment VARCHAR;
    ALTER TABLE reviews ADD COLUMN IF NOT EXISTS sentiment_score FLOAT;
""")

# Récupère les avis non encore traités
df = conn.execute("""
    SELECT review_id, text FROM reviews
    WHERE sentiment IS NULL
    LIMIT 5000
""").df()

print(f"🔄 {len(df)} avis à traiter...")

# Prédiction par batch
results = []
for _, row in tqdm(df.iterrows(), total=len(df)):
    pred = predict_sentiment(row["text"])
    results.append({
        "review_id": row["review_id"],
        "langue": pred["langue"],
        "sentiment": pred["sentiment"],
        "sentiment_score": pred["score"]
    })

# Mise à jour de la base
results_df = pd.DataFrame(results)
conn.register("results_df", results_df)
conn.execute("""
    UPDATE reviews
    SET 
        langue = r.langue,
        sentiment = r.sentiment,
        sentiment_score = r.sentiment_score
    FROM results_df r
    WHERE reviews.review_id = r.review_id
""")

print("✅ Base enrichie !")
print(conn.execute("SELECT sentiment, COUNT(*) FROM reviews WHERE sentiment IS NOT NULL GROUP BY 1").df())