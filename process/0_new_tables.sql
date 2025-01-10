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

CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name TEXT UNIQUE
);

INSERT INTO teams (team_name)
SELECT DISTINCT team
FROM batting;

ALTER TABLE teams ADD COLUMN team_abbrev TEXT;

UPDATE teams
SET team_abbrev = UPPER(
    (SELECT string_agg(SUBSTRING(word, 1, 1), '')
     FROM regexp_split_to_table(team_name, '\s+') AS word)
);