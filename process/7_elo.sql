ALTER TABLE elo_ratings
ADD COLUMN team_1_total INT,
ADD COLUMN team_2_total INT,
ADD COLUMN team_1_wickets INT,
ADD COLUMN team_2_wickets INT,
ADD COLUMN team_1_extras INT,
ADD COLUMN team_2_extras INT,
ADD COLUMN team_1_dots INT,
ADD COLUMN team_2_dots INT,
ADD COLUMN team_1_boundaries INT,
ADD COLUMN team_2_boundaries INT,
ADD COLUMN team_1_balls INT,
ADD COLUMN team_2_balls INT;

UPDATE elo_ratings SET team_1_total = total.total FROM total WHERE elo_ratings.match_id = total.match_id AND elo_ratings.team_1_id = total.team_id;
UPDATE elo_ratings SET team_2_total = total.total FROM total WHERE elo_ratings.match_id = total.match_id AND elo_ratings.team_2_id = total.team_id;

UPDATE elo_ratings SET team_1_wickets = total.wickets FROM total WHERE elo_ratings.match_id = total.match_id AND elo_ratings.team_1_id = total.team_id;
UPDATE elo_ratings SET team_2_wickets = total.wickets FROM total WHERE elo_ratings.match_id = total.match_id AND elo_ratings.team_2_id = total.team_id;

UPDATE elo_ratings SET team_1_extras = extras.extras FROM extras WHERE elo_ratings.match_id = extras.match_id AND elo_ratings.team_1_id = extras.team_id;
UPDATE elo_ratings SET team_2_extras = extras.extras FROM extras WHERE elo_ratings.match_id = extras.match_id AND elo_ratings.team_2_id = extras.team_id;

UPDATE elo_ratings SET team_1_boundaries = source.boundaries FROM (SELECT match_id, team_id, SUM(fours + sixes) AS boundaries FROM batting GROUP BY match_id, team_id) AS source WHERE elo_ratings.match_id = source.match_id AND elo_ratings.team_1_id = source.team_id;

UPDATE elo_ratings SET team_2_boundaries = source.boundaries FROM (SELECT match_id, team_id, SUM(fours + sixes) AS boundaries FROM batting GROUP BY match_id, team_id) AS source WHERE elo_ratings.match_id = source.match_id AND elo_ratings.team_2_id = source.team_id;

UPDATE elo_ratings SET team_1_balls = total.balls FROM total WHERE elo_ratings.match_id = total.match_id AND elo_ratings.team_1_id = total.team_id;
UPDATE elo_ratings SET team_2_balls = total.balls FROM total WHERE elo_ratings.match_id = total.match_id AND elo_ratings.team_2_id = total.team_id;

UPDATE elo_ratings SET team_1_dots = source.dots FROM (SELECT match_id, team_id, SUM(dots) AS dots FROM bowling GROUP BY match_id, team_id) AS source WHERE elo_ratings.match_id = source.match_id AND elo_ratings.team_1_id = source.team_id;
UPDATE elo_ratings SET team_2_dots = source.dots FROM (SELECT match_id, team_id, SUM(dots) AS dots FROM bowling GROUP BY match_id, team_id) AS source WHERE elo_ratings.match_id = source.match_id AND elo_ratings.team_2_id = source.team_id;