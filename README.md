# 🍕 Restaurant Sentiment Dashboard

![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)

> Pipeline NLP multilingue pour l'analyse de sentiments d'avis restaurants (FR/EN), avec API REST et dashboard interactif.

---

## 📸 Demo

![demo](demo.gif)

---

## 🏗 Architecture

```
Yelp Dataset (200k avis)
        │
        ▼
   DuckDB (SQL)          ← exploration & stockage
        │
        ▼
HuggingFace Transformers ← classification multilingue
(tabularisai/multilingual-sentiment-analysis)
        │
        ▼
   FastAPI REST API      ← exposition du modèle
        │
        ▼
 Streamlit Dashboard     ← visualisation interactive
```

---

## 🛠 Stack

| Composant | Technologie |
|---|---|
| Stockage & SQL | DuckDB, Pandas |
| NLP | HuggingFace Transformers |
| Détection de langue | langdetect |
| API REST | FastAPI, Uvicorn |
| Dashboard | Streamlit, Plotly |
| Tests | pytest, httpx |
| CI/CD | GitHub Actions |

---

## 📊 Résultats

- **200 000 avis** analysés (dataset Yelp)
- **5 niveaux de sentiment** : Very Negative → Very Positive
- **Multilingue** : français et anglais
- **API REST** documentée via Swagger (`/docs`)

---

## 🚀 Lancer le projet

### Prérequis

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO
cd YOUR_REPO
pip install -r requirements.txt
```

### 1. Préparer la base de données

```bash
# Charger et enrichir les données Yelp
python sql/enrich.py
```

### 2. Lancer l'API

```bash
uvicorn api.main:app --reload
# → http://localhost:8000/docs
```

### 3. Lancer le dashboard

```bash
streamlit run app/dashboard.py
# → http://localhost:8501
```

---

## 🔌 Endpoints API

| Méthode | Route | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/predict` | Analyse un texte |
| GET | `/stats` | Statistiques globales |
| GET | `/reviews` | Explorer les avis |

Exemple :
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Excellent restaurant, je recommande !"}'
```

Réponse :
```json
{
  "text": "Excellent restaurant, je recommande !",
  "langue": "fr",
  "sentiment": "Very Positive",
  "score": 0.91
}
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

Les tests couvrent tous les endpoints de l'API et tournent automatiquement via GitHub Actions à chaque push.

---

## 📁 Structure

```
├── model/
│   └── predict.py          # inférence HuggingFace
├── api/
│   └── main.py             # API REST FastAPI
├── app/
│   └── dashboard.py        # dashboard Streamlit + Plotly
├── sql/
│   └── enrich.py           # enrichissement DuckDB
├── tests/
│   └── test_api.py         # tests pytest
├── .github/
│   └── workflows/
│       └── ci.yml          # pipeline CI/CD
├── requirements.txt
└── README.md
```

---

## 💡 Choix techniques

**DuckDB** — permet d'interroger des fichiers JSON/CSV directement en SQL sans serveur, idéal pour l'exploration de données.

**tabularisai/multilingual-sentiment-analysis** — modèle entraîné sur des avis multilingues, supporte le français et l'anglais avec 5 niveaux de sentiment.

**FastAPI** — génère automatiquement la documentation Swagger, typage fort avec Pydantic, performances élevées.

**langdetect** — détection de langue légère et rapide, suffisante pour distinguer FR/EN sur des avis courts.
