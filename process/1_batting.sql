ALTER TABLE batting
ADD COLUMN player_id INT,
ADD COLUMN team_id INT,
ADD COLUMN pts INT;

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
SET strike_rate = CASE 
    WHEN balls = 0 THEN 0 
    ELSE (runs * 100) / balls 
END;

UPDATE batting SET pts = runs + fours + (2 * sixes);
UPDATE batting SET pts = pts + 4 WHERE runs >= 30 AND runs < 50;
UPDATE batting SET pts = pts + 8 WHERE runs >= 50 AND runs < 100;
UPDATE batting SET pts = pts + 16 WHERE runs > 100;
UPDATE batting SET pts = pts - 2 WHERE runs = 0 AND balls > 0;

UPDATE batting SET pts = pts + 6 WHERE (strike_rate >= 170) AND balls >= 10;
UPDATE batting SET pts = pts + 4 WHERE (strike_rate >= 150 AND strike_rate < 170) AND balls >= 10;
UPDATE batting SET pts = pts + 2 WHERE (strike_rate >= 130 AND strike_rate < 150) AND balls >= 10;
UPDATE batting SET pts = pts - 2 WHERE (strike_rate >= 60 AND strike_rate < 70) AND balls >= 10;
UPDATE batting SET pts = pts - 4 WHERE (strike_rate >= 50 AND strike_rate < 60) AND balls >= 10;
UPDATE batting SET pts = pts - 6 WHERE (strike_rate < 50) AND balls >= 10;