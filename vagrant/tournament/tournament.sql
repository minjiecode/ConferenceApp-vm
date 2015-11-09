-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE scoreboard (
	id		serial primary key,
	name 	text,
	wins	integer,
	matches	integer
	);

-- show the full record in the database ordered by the wins
CREATE VIEW rank AS 
	SELECT *
	FROM scoreboard
	ORDER BY wins desc;