import os
os.environ["HF_HOME"] = "./models"
os.environ["HF_HUB_CACHE"] = "./models/hub"
os.environ["TRANSFORMERS_CACHE"] = "./models"

import pytest
import duckdb
from fastapi.testclient import TestClient

TEST_DB = "reviews_test.db"

@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    conn = duckdb.connect(TEST_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id VARCHAR, stars INTEGER, text VARCHAR,
            date DATE, useful INTEGER, langue VARCHAR,
            sentiment VARCHAR, sentiment_score FLOAT
        )
    """)
    conn.execute("""
        INSERT INTO reviews VALUES
        ('r1', 5, 'Amazing food!', '2023-01-01', 1, 'en', 'Very Positive', 0.95),
        ('r2', 1, 'Terrible experience.', '2023-01-02', 0, 'en', 'Very Negative', 0.88),
        ('r3', 3, 'It was okay.', '2023-01-03', 0, 'en', 'Neutral', 0.60)
    """)
    conn.close()

    # Redirige l'app vers la base de test
    import api.main as main
    main.conn = duckdb.connect(TEST_DB, read_only=True)

    yield

    os.remove(TEST_DB)

from api.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200

def test_predict_english():
    res = client.post("/predict", json={"text": "Amazing food!"})
    assert res.status_code == 200
    assert res.json()["sentiment"] in ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"]
    assert res.json()["score"] > 0

def test_predict_french():
    res = client.post("/predict", json={"text": "Vraiment décevant."})
    assert res.status_code == 200
    assert res.json()["langue"] == "fr"

def test_stats():
    res = client.get("/stats")
    assert res.status_code == 200
    assert "distribution" in res.json()

def test_reviews():
    res = client.get("/reviews?limit=5")
    assert res.status_code == 200
    assert len(res.json()) <= 5