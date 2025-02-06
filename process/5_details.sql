ALTER TABLE details
ADD COLUMN team_1_id INT,
ADD COLUMN team_2_id INT,
ADD COLUMN winner TEXT,
ADD COLUMN winner_id INT,
ADD COLUMN is_playoff BOOLEAN,
ADD COLUMN stadium_id INT;

ALTER TABLE details
ALTER COLUMN date TYPE DATE USING date::DATE;

ALTER TABLE details
ALTER COLUMN season TYPE INTEGER USING season::INTEGER;

UPDATE details SET team_1 = 'Royal Challengers Bengaluru' WHERE team_1 = 'Royal Challengers Bangalore';
UPDATE details SET team_1 = 'Delhi Capitals' WHERE team_1 = 'Delhi Daredevils';
UPDATE details SET team_1 = 'Punjab Kings' WHERE team_1 = 'Kings XI Punjab';

UPDATE details SET team_2 = 'Royal Challengers Bengaluru' WHERE team_2 = 'Royal Challengers Bangalore';
UPDATE details SET team_2 = 'Delhi Capitals' WHERE team_2 = 'Delhi Daredevils';
UPDATE details SET team_2 = 'Punjab Kings' WHERE team_2 = 'Kings XI Punjab';

UPDATE details
SET team_1_id = teams.team_id
FROM teams
WHERE details.team_1 = teams.team_name;

UPDATE details
SET team_2_id = teams.team_id
FROM teams
WHERE details.team_2 = teams.team_name;

UPDATE details
SET winner = total.team
FROM total
WHERE details.match_id = total.match_id AND total.winner=TRUE;

UPDATE details
SET winner_id = teams.team_id
FROM teams
WHERE details.winner = teams.team_name;

UPDATE details
SET is_playoff = 
    CASE 
        WHEN match_type ~* '^[0-9].*match' THEN FALSE
        ELSE TRUE
    END;

WITH points AS (
    SELECT
    match_id,
    team_id,
    SUM(pts) AS pts 
    FROM batting
    GROUP BY match_id, team_id
)
UPDATE details
SET team_1_pts = pts
FROM points
WHERE details.match_id = points.match_id
AND points.team_id = details.team_1_id;

WITH points AS (
    SELECT
    match_id,
    team_id,
    SUM(pts) AS pts
    FROM batting
    GROUP BY match_id, team_id
)
UPDATE details
SET team_2_pts = pts
FROM points
WHERE details.match_id = points.match_id
AND points.team_id = details.team_2_id;

WITH points AS (
    SELECT
    match_id,
    team_id,
    SUM(pts) AS pts 
    FROM bowling
    GROUP BY match_id, team_id
)
UPDATE details
SET team_1_pts = team_1_pts + pts
FROM points
WHERE details.match_id = points.match_id
AND points.team_id = details.team_1_id;

WITH points AS (
    SELECT
    match_id,
    team_id,
    SUM(pts) AS pts
    FROM bowling
    GROUP BY match_id, team_id
)
UPDATE details
SET team_2_pts = team_2_pts + pts
FROM points
WHERE details.match_id = points.match_id
AND points.team_id = details.team_2_id;

UPDATE details
SET stadium_id = stadiums.stadium_id
FROM stadiums
WHERE details.stadium = stadiums.stadium_name;