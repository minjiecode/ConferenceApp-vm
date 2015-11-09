#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("UPDATE scoreboard SET matches = NULL")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from scoreboard")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute ("SELECT COUNT(name) FROM scoreboard")
    count = c.fetchall()
    DB.close()
    return count[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute ("INSERT INTO scoreboard (name, wins, matches) values (%s, 0, 0)",
                (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute ("SELECT * from rank")
    rows = c.fetchall()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    update_winner = "UPDATE scoreboard SET wins=wins+1, matches=matches+1 WHERE id = %s "
    update_loser = "UPDATE scoreboard SET matches=matches+1 WHERE id = %s "
    c.execute(update_winner, (winner,))     # update the wins and matches of the winner
    c.execute(update_loser, (loser,))       # update the matches of the loser
    DB.commit()
    DB.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ranking = playerStandings()         # get the current playstanding
    totalplayers = countPlayers()       # get the number of the players
    pairs = totalplayers/2              # caculate the number of pairs
    pairing = []                        # initiate the list
    for k in range(pairs):
        pairing.append((ranking[2*k][0], ranking[2*k][1], ranking[2*k+1][0], ranking[2*k+1][1]))
    return pairing

