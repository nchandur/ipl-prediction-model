CREATE TABLE points (
    team_id INT,
    team_name TEXT,
    season INT,
    matches INT,
    win INT,
    loss INT,
    no_result INT,
    pts INT,
    win_per DECIMAL(10, 3)
);

INSERT INTO points (team_id, season, win)
SELECT 
    winner_id AS team_id,
    season,
    COUNT(*) AS win
FROM 
    details
WHERE 
    winner_id IS NOT NULL AND is_playoff = FALSE
GROUP BY 
    winner_id, season;


INSERT INTO points (team_id, season, loss)
SELECT 
    team_id,
    season,
    COUNT(*) AS loss
FROM (
    SELECT 
        team_1_id AS team_id,
        season
    FROM 
        details
    WHERE 
        winner_id != team_1_id
        AND winner_id IS NOT NULL AND is_playoff = FALSE
    UNION ALL
    SELECT 
        team_2_id AS team_id,
        season
    FROM 
        details
    WHERE 
        winner_id != team_2_id
        AND winner_id IS NOT NULL AND is_playoff = FALSE
) AS losses
GROUP BY 
    team_id, season;

UPDATE points
SET loss = subquery.loss
FROM (
    SELECT team_id, season, SUM(loss) AS loss
    FROM points
    GROUP BY team_id, season
) AS subquery
WHERE points.team_id = subquery.team_id
AND points.season = subquery.season;

DELETE FROM points WHERE win IS NULL;

UPDATE points
SET no_result = subquery.no_result
FROM (
    SELECT 
        team_id,
        season,
        COUNT(*) AS no_result
    FROM (
        SELECT 
            team_1_id AS team_id,
            season
        FROM 
            details
        WHERE 
            winner IS NULL
        UNION ALL
        SELECT 
            team_2_id AS team_id,
            season
        FROM 
            details
        WHERE 
            winner IS NULL
    ) AS no_result_matches
    GROUP BY 
        team_id, season
) AS subquery
WHERE 
    points.team_id = subquery.team_id
    AND points.season = subquery.season;

UPDATE points SET no_result = 0 WHERE no_result IS NULL;

UPDATE points SET matches = win + loss + no_result;

UPDATE points SET team_name = teams.team_name FROM teams WHERE points.team_id = teams.team_id;

UPDATE points SET pts = (2 * win) + no_result;

UPDATE points SET win_per = win::DECIMAL(10, 2) / matches::DECIMAL(10, 2);