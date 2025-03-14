ALTER TABLE batting
ADD COLUMN player_id INT,
ADD COLUMN team_id INT,
ADD COLUMN date DATE;

ALTER TABLE batting
ALTER COLUMN innings TYPE INTEGER USING innings::INTEGER;

UPDATE batting set runs = NULL WHERE runs LIKE '-%';
ALTER TABLE batting
ALTER COLUMN runs TYPE INTEGER USING runs::INTEGER;

UPDATE batting set balls = NULL WHERE balls LIKE '-%';
ALTER TABLE batting
ALTER COLUMN balls TYPE INTEGER USING balls::INTEGER;

ALTER TABLE batting
ALTER COLUMN minutes_played TYPE INTEGER USING minutes_played::INTEGER;

UPDATE batting set fours = NULL WHERE fours LIKE '-%';
ALTER TABLE batting
ALTER COLUMN fours TYPE INTEGER USING fours::INTEGER;

UPDATE batting set sixes = NULL WHERE sixes LIKE '-%';
ALTER TABLE batting
ALTER COLUMN sixes TYPE INTEGER USING sixes::INTEGER;

UPDATE batting set strike_rate = NULL WHERE strike_rate LIKE '-%';
ALTER TABLE batting
ALTER COLUMN strike_rate TYPE DECIMAL(10, 2) USING strike_rate::DECIMAL(10, 2);

UPDATE batting
SET player_id = players.player_id
FROM players
WHERE batting.player_name = players.player_name;

UPDATE batting SET team = 'Royal Challengers Bengaluru' WHERE team = 'Royal Challengers Bangalore';
UPDATE batting SET team = 'Delhi Capitals' WHERE team = 'Delhi Daredevils';
UPDATE batting SET team = 'Punjab Kings' WHERE team = 'Kings XI Punjab';

UPDATE batting
SET team_id = teams.team_id
FROM teams
WHERE batting.team = teams.team_name;

UPDATE batting
SET date = details.date::DATE
FROM details
WHERE batting.match_id = details.match_id;

UPDATE batting 
SET strike_rate = CASE 
    WHEN balls = 0 THEN 0 
    ELSE (runs * 100) / balls 
END;