WITH GoldMedalists AS (
    SELECT DISTINCT m.athlete_id, m."event"
    FROM weightlifting_olympians.medal m
    INNER JOIN weightlifting_olympians.event e ON
    m.event_id = e.event_id
    WHERE m.medal = 'Gold'
)
SELECT
    g.event,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY a.weight / a.height) AS Q1,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY a.weight / a.height) AS Median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY a.weight / a.height) AS Q3
FROM
    weightlifting_olympians.athlete a
JOIN
    GoldMedalists g ON a.athlete_id = g.athlete_id
GROUP BY
    g.event;