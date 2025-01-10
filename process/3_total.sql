ALTER TABLE total
ADD COLUMN team_id INT,
ADD COLUMN winner BOOLEAN;

ALTER TABLE total
ALTER COLUMN overs TYPE DECIMAL(10, 1) USING overs::DECIMAL(10, 1);

UPDATE total
SET run_rate = SUBSTRING(run_rate FROM '^[^,]+');

ALTER TABLE total
ALTER COLUMN run_rate TYPE DECIMAL(10, 2) USING run_rate::DECIMAL(10, 2);

ALTER TABLE total
ALTER COLUMN total TYPE INTEGER USING total::INTEGER;

ALTER TABLE total
ALTER COLUMN wickets TYPE INTEGER USING wickets::INTEGER;

ALTER TABLE total
ALTER COLUMN innings TYPE INTEGER USING innings::INTEGER;

UPDATE total
SET team_id = teams.team_id
FROM teams
WHERE total.team = teams.team_name;

WITH ranked_matches AS (
    SELECT 
        match_id,
        team_id,
        total,
        overs,
        ROW_NUMBER() OVER (PARTITION BY match_id ORDER BY total DESC, overs ASC) AS rank
    FROM total
)
UPDATE total
SET winner = CASE
                WHEN ranked_matches.rank = 1 THEN TRUE
                ELSE FALSE
             END
FROM ranked_matches
WHERE total.match_id = ranked_matches.match_id
AND total.team_id = ranked_matches.team_id;
