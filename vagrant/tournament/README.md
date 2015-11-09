##TOURNAMENT RESULT

**Tournament Result** intend to help users to easily manage a swiss-style tournament. 
The current version only supports even number of players. 
- Register Players 
- Record Match Result
- Check Player Standing
- Pair Players for match

> \**This is a project for the Udacity Nanodegree Course*

### Installation

1. Clone this repository `git clone https://github.com/minjiecode/fullstack-nanodegree-vm.git`
2. Set your working directory to `etc/vagrant`
3. Launch Vagrant by calling: `vagrant up` and `vagrant ssh`
4. Set your working directory to `etc/vagrant/tournament`
5. Launch psql by calling: `psql`
6. Create and connect to the database, create tables and views by calling: `\i tournament.sql;`
7. Close psql by calling: `\q`
8. From bash, confirm tests are passed by running: `python tournament_test.py`

### Functions

- `deleteMatches()` Remove all the matches records from the database.
- `countPlayers()`  Returns the number of players currently registered.
- `registerPlayer(name)`Adds a player to the tournament database.`name` must be a string. 
- `playerStandings()`Returns a list of the players and their win records, sorted by wins. 
- `reportMatch(winner_id, loser_id)`  Populate the matches table and record the winner and loser.
- `swissPairings()` Returns a list of pairs of players for the next round of a match.

### Example

    $ python -c "from tournament import *; registerPlayer("Mark")"    

### Software Stack
- Vagrant
- VirtualBox
- PostgreSQL
- Python

### Include
- tournament.py
- tournament.sql
- tournament_test.py
- readme.md


