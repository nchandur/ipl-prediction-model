ALTER TABLE details
ADD COLUMN team_1_id INT,
ADD COLUMN team_2_id INT,
ADD COLUMN winner TEXT,
ADD COLUMN winner_id INT,
ADD COLUMN is_playoff BOOLEAN;

ALTER TABLE details
ALTER COLUMN date TYPE DATE USING date::DATE;

ALTER TABLE details
ALTER COLUMN season TYPE INTEGER USING season::INTEGER;

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