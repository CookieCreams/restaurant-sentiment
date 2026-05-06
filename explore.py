import duckdb

conn = duckdb.connect("reviews.db")

# Charger le JSON Yelp directement
conn.execute("""
    CREATE TABLE reviews AS
    SELECT 
        review_id,
        stars,
        text,
        date,
        useful
    FROM read_json_auto('YELP_JSON/yelp_academic_dataset_review.json')
    LIMIT 100000
""")

# Premières explorations SQL
conn.execute("""
    SELECT 
        stars,
        COUNT(*) as nb_avis,
        AVG(LENGTH(text)) as longueur_moyenne
    FROM reviews
    GROUP BY stars
    ORDER BY stars
""").df()