-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--
-- This table stores information about players "id" is unique ID, "name" is the player's name, "created" is when the record was created.
CREATE TABLE players(
id SERIAL PRIMARY KEY,
name VARCHAR(255) NOT NULL,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
--
-- Table stores information about the tournament. 
-- the name, start_date, end_date and details fields store information about a tournament
CREATE TABLE tournaments(
id SERIAL PRIMARY KEY,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
name VARCHAR(255) NOT NULL,
start_date DATE,
end_date DATE,
details TEXT
);
--
-- create 1st tournament --
INSERT INTO tournaments (id, name, start_date, end_date, details) VALUES ('1', 'One', '2015-10-10', '2015-11-10', 'Swiss style tournament');
-- Table stores tournament matches
CREATE TABLE matches(
id SERIAL PRIMARY KEY,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
match_date DATE NOT NULL,
tournament_id INTEGER REFERENCES tournaments(id) ON DELETE RESTRICT NOT NULL,
player1_id INTEGER REFERENCES players(id) ON DELETE RESTRICT NOT NULL,
player2_id INTEGER REFERENCES players(id) ON DELETE RESTRICT,
win_player_id INTEGER REFERENCES players(id) ON DELETE RESTRICT DEFAULT NULL,
CONSTRAINT u_constraint UNIQUE (tournament_id, player1_id, player2_id)
);
--
-- Table stores information on players who enrolled in tournament
CREATE TABLE tournament_players(
tournament_id INTEGER REFERENCES tournaments(id) ON DELETE RESTRICT NOT NULL,
player_id INTEGER REFERENCES players(id) ON DELETE RESTRICT NOT NULL,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
register_date DATE,
PRIMARY KEY(tournament_id, player_id)
);
--


