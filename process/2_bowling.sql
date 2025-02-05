ALTER TABLE bowling
ADD COLUMN player_id INT,
ADD COLUMN team_id INT,
ADD COLUMN balls INT,
ADD COLUMN date DATE;

ALTER TABLE bowling
ALTER COLUMN overs TYPE DECIMAL(10, 1) USING overs::DECIMAL(10, 1);

ALTER TABLE bowling
ALTER COLUMN m TYPE INTEGER USING m::INTEGER;

ALTER TABLE bowling
ALTER COLUMN runs TYPE INTEGER USING runs::INTEGER;

ALTER TABLE bowling
ALTER COLUMN wickets TYPE INTEGER USING wickets::INTEGER;

ALTER TABLE bowling
ALTER COLUMN econ TYPE DECIMAL(10, 2) USING econ::DECIMAL(10, 2);

ALTER TABLE bowling
ALTER COLUMN dots TYPE INTEGER USING dots::INTEGER;

ALTER TABLE bowling
ALTER COLUMN fours TYPE INTEGER USING fours::INTEGER;

ALTER TABLE bowling
ALTER COLUMN sixes TYPE INTEGER USING sixes::INTEGER;

ALTER TABLE bowling
ALTER COLUMN wides TYPE INTEGER USING wides::INTEGER;

ALTER TABLE bowling
ALTER COLUMN no_balls TYPE INTEGER USING no_balls::INTEGER;

ALTER TABLE bowling
ALTER COLUMN innings TYPE INTEGER USING innings::INTEGER;

UPDATE bowling
SET player_id = players.player_id
FROM players
WHERE bowling.player_name = players.player_name;

UPDATE bowling SET team = 'Royal Challengers Bengaluru' WHERE team = 'Royal Challengers Bangalore';
UPDATE bowling SET team = 'Delhi Capitals' WHERE team = 'Delhi Daredevils';
UPDATE bowling SET team = 'Punjab Kings' WHERE team = 'Kings XI Punjab';

UPDATE bowling
SET team_id = teams.team_id
FROM teams
WHERE bowling.team = teams.team_name;

UPDATE bowling
SET date = details.date::DATE
FROM details
WHERE bowling.match_id = details.match_id;

UPDATE bowling SET balls = (FLOOR(overs) * 6) + ((overs - FLOOR(overs)) * 10);  

UPDATE bowling 
SET econ = CASE 
    WHEN balls = 0 THEN 0 
    ELSE (runs * 6) / balls 
END;