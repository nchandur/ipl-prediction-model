CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    player_name TEXT UNIQUE
);

INSERT INTO players (player_name)
SELECT DISTINCT player_name
FROM (
    SELECT player_name FROM batting
    UNION
    SELECT player_name FROM bowling
) AS combined_players;

UPDATE players SET player_name = TRIM(player_name);

CREATE TABLE teams (
    team_name TEXT UNIQUE
);

INSERT INTO teams (team_name)
SELECT DISTINCT team
FROM batting;

UPDATE teams SET team_name = TRIM(team_name);
DELETE FROM teams WHERE team_name IN ('Royal Challengers Bangalore', 'Delhi Daredevils', 'Kings XI Punjab');

ALTER TABLE teams 
ADD COLUMN team_id SERIAL,
ADD COLUMN team_abbrev TEXT;

UPDATE teams
SET team_abbrev = UPPER(
    (SELECT string_agg(SUBSTRING(word, 1, 1), '')
     FROM regexp_split_to_table(team_name, '\s+') AS word)
);

UPDATE details SET stadium = REPLACE(stadium, 'Bangalore', 'Bengaluru') WHERE stadium ILIKE '%bangalore%';

CREATE TABLE stadiums (
    stadium_id SERIAL PRIMARY KEY, 
    stadium_name TEXT
);

INSERT INTO stadiums (stadium_name)
SELECT DISTINCT stadium
FROM details;