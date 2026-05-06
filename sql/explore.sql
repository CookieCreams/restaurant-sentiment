-- 1. Distribution des notes
SELECT stars, COUNT(*) as nb, ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(), 1) as pct
FROM reviews GROUP BY stars ORDER BY stars;

-- 2. Évolution mensuelle du sentiment moyen
SELECT DATE_TRUNC('month', date) as mois, ROUND(AVG(stars), 2) as note_moyenne
FROM reviews GROUP BY 1 ORDER BY 1;

-- 3. Longueur des avis selon la note
SELECT stars, ROUND(AVG(LENGTH(text))) as longueur_moyenne, COUNT(*) as nb
FROM reviews GROUP BY stars ORDER BY stars;

-- 4. Avis suspects (courts + extrêmes)
SELECT stars, text, LENGTH(text) as longueur
FROM reviews
WHERE LENGTH(text) < 50 AND stars IN (1, 5)
ORDER BY longueur LIMIT 20;

-- 5. Activité par jour de la semaine
SELECT DAYNAME(date) as jour, COUNT(*) as nb_avis, ROUND(AVG(stars), 2) as note_moy
FROM reviews GROUP BY 1 ORDER BY 2 DESC;