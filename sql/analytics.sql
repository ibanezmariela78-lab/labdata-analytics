-- Consultas de ejemplo sobre el esquema operacional PostgreSQL.
-- La regla de ±5 puntos porcentuales es demostrativa, no una especificación GMP.
SELECT product,
       COUNT(*) AS samples,
       ROUND(AVG(assay_pct), 2) AS mean_assay_pct,
       ROUND(AVG(assay_pct - target), 2) AS mean_deviation,
       SUM(CASE WHEN ABS(assay_pct - target) > 5 THEN 1 ELSE 0 END) AS out_of_spec
FROM laboratory_samples
GROUP BY product
ORDER BY product;

SELECT DATE_TRUNC('month', sampled_at)::date AS month,
       COUNT(*) AS samples,
       ROUND(AVG(assay_pct), 2) AS mean_assay_pct
FROM laboratory_samples
GROUP BY 1
ORDER BY 1;

SELECT batch, product, COUNT(*) AS samples,
       ROUND(AVG(assay_pct), 2) AS mean_assay_pct
FROM laboratory_samples
GROUP BY batch, product
ORDER BY samples DESC, batch;
