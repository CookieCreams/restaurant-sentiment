import os
os.environ["HF_HOME"] = "./models"
os.environ["HF_HUB_CACHE"] = "./models/hub"
os.environ["TRANSFORMERS_CACHE"] = "./models"

from transformers import pipeline
from langdetect import detect

# Un seul modèle multilingue pour tout
# classifier = pipeline(
#     "sentiment-analysis",
#     model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
# )

classifier = pipeline(
    "sentiment-analysis",
    model="tabularisai/multilingual-sentiment-analysis"
)

def predict_sentiment(text: str) -> dict:
    try:
        lang = detect(text)
    except:
        lang = "unknown"
    
    result = classifier(text[:512])[0]
    
    return {
        "text": text,
        "langue": lang,
        "sentiment": result["label"],  # positive / negative / neutral
        "score": round(result["score"], 3)
    }

if __name__ == "__main__":
    tests = [
        "This restaurant was absolutely amazing, best pizza ever!",
        "Vraiment décevant, service lent et nourriture froide.",
        "It was okay, nothing special but not bad either.",
        "Les pâtes étaient excellentes, je recommande vivement !"
    ]
    for t in tests:
        print(predict_sentiment(t))