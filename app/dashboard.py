import os
os.environ["HF_HOME"] = "./models"
os.environ["HF_HUB_CACHE"] = "./models/hub"
os.environ["TRANSFORMERS_CACHE"] = "./models"

import streamlit as st
import requests
import plotly.express as px
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Restaurant Sentiment Dashboard", page_icon="🍕", layout="wide")
st.title("🍕 Restaurant Reviews — Sentiment Dashboard")

# --- STATS GLOBALES ---
stats = requests.get(f"{API_URL}/stats").json()

dist_df = pd.DataFrame(stats["distribution"])
note_df = pd.DataFrame(stats["par_note"])
lang_df = pd.DataFrame(stats["par_langue"])

# Ordre des sentiments
order = ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]
colors = {
    "Very Negative": "#d62728",
    "Negative": "#ff7f0e",
    "Neutral": "#7f7f7f",
    "Positive": "#2ca02c",
    "Very Positive": "#1f77b4"
}

col1, col2, col3 = st.columns(3)

with col1:
    fig = px.bar(
        dist_df, x="sentiment", y="nb",
        title="Distribution des sentiments",
        color="sentiment",
        color_discrete_map=colors,
        category_orders={"sentiment": order}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.bar(
        note_df, x="stars", y="score_moyen",
        title="Score de confiance moyen par note",
        color_discrete_sequence=["#1f77b4"]
    )
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    fig3 = px.pie(
        lang_df, names="langue", values="nb",
        title="Répartition par langue"
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- ANALYSE EN TEMPS RÉEL ---
st.subheader("🔍 Analyser un avis")
col_input, col_result = st.columns([2, 1])

with col_input:
    user_text = st.text_area("Colle un avis ici :", height=100)
    if st.button("Analyser"):
        if user_text:
            res = requests.post(f"{API_URL}/predict", json={"text": user_text}).json()
            with col_result:
                sentiment = res["sentiment"]
                color = colors.get(sentiment, "#333")
                st.markdown(f"### {sentiment}")
                st.progress(res["score"])
                st.caption(f"Confiance : {res['score']*100:.1f}% | Langue : {res['langue']}")

st.markdown("---")

# --- EXPLORATEUR D'AVIS ---
st.subheader("📋 Explorer les avis")
col_filter, _ = st.columns([1, 3])

with col_filter:
    selected = st.selectbox("Filtrer par sentiment :", ["Tous"] + order)

sentiment_param = None if selected == "Tous" else selected
reviews = requests.get(f"{API_URL}/reviews", params={"sentiment": sentiment_param, "limit": 10}).json()
reviews_df = pd.DataFrame(reviews)[["stars", "sentiment", "sentiment_score", "text", "date"]]
st.dataframe(reviews_df, use_container_width=True)