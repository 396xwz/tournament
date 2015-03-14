#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import datetime 
import bleach
import psycopg2, psycopg2.extras, psycopg2.errorcodes
import inflect 

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except psycopg2.Error as e:
	print "Database connect problem"
      	exit() 


def deleteMatches():
   """Remove all the match records from the database."""
   try:  
    DB = connect();
    cur = DB.cursor();
    DEL = cur.execute("DELETE FROM matches *;")
    DB.commit()
    DB.close()
   except psycopg2.Error as e:
    print "Database Delete Issue"
    exit()

def deletePlayers():
   """Remove all the player records from the database."""
   try:
    DB = connect();
    cur = DB.cursor();
    DEL = cur.execute("DELETE FROM players *;")
    DB.commit()
    DB.close()
   except psycopg2.Error as e:
    print "Database Delete Issue"
    exit()
def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect();
    """ Open a cursor to perform database operations """
    cur = DB.cursor();
    """Returns the number of players currently registered."""
    try: 
        cur.execute("SELECT COUNT(*) FROM players AS num;")
        result = cur.fetchone()
    	DB.close()
        WordCount = inflect.engine()
	TextCount = WordCount.number_to_words(result)
        if TextCount != "zero":
         return result[0] 
        else:
         return 0 
    except psycopg2.Error as e:
   	print "Failed to count players"	

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    """ insert into players values ('12350', 'Sam Zine', 'szine@foo.com', '1971-07-11');"""
    
    DB = connect();
    cur = DB.cursor();
    cur.execute("INSERT INTO players (name) VALUES (%s) RETURNING id",(bleach.clean(name),))
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
    cur = DB.cursor()
    """get players and number of wins """
    cur.execute("""SELECT players.id, players.name, COUNT(matches.id) AS wins FROM players
        LEFT JOIN matches ON players.id = matches.win_player_id GROUP BY players.id 
        ORDER BY wins DESC
	      """)

    wins = cur.fetchall()
    """ get players and number of matches """
    cur.execute("""SELECT players.id, players.name, COUNT(matches.id) AS matches FROM players LEFT JOIN matches ON players.id = matches.player1_id OR players.id = matches.player2_id GROUP BY players.id ORDER BY players.id""")
    records = cur.fetchall()
    DB.close()
    """get  list of tuples that merges players wins and matches played"""
    result = []
    for unit in wins:
	for row in records:
		if unit[0] == row[0]:
			result.append((
			unit[0],
			unit[1],
			unit[2],
			row[2]
			))
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    #connect to DB
    DB = connect()
    con = DB.cursor() 
    #con.execute("SELECT COUNT(id) FROM matches WHERE tournament_id = %s AND player1_id = %s AND player2_id IS %s", (tournament_id, player_one, None))
    #result = con.fetchone()
    tournament_id=1
    match_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    try:
	con.execute("INSERT INTO matches(match_date, tournament_id, player1_id, player2_id, win_player_id) VALUES (%s,%s,%s,%s,%s)",
	( bleach.clean(match_date),
	tournament_id,
	winner,
	loser,
	winner
	))
	DB.commit()
    except psycopg2.IntegrityError:
	return "EROR: Both Players cannot face each other twice"
    DB.close()

def playerCheck(player_one,player_two):
	"""
	Check if two players can play against each another
	"""
	if player_one == player_two:
		return False
	DB = connect()
	con = DB.cursor()
	#the first case is player1 and player2 are in order
	con.execute("SELECT COUNT(id) FROM matches WHERE player1_id = %s AND player2_id = %s", (player_one,player_two))
	ret1 = con.fetchone()
	#the second case is where player1 and player2 are in reverse order
	con.execute("SELECT COUNT(id) FROM matches WHERE player2_id = %s AND player1_id = %s", (player_one,player_two))
	ret2 = con.fetchone()
	DB.close()
        if ret1[0] > 0 or ret2[0] > 0:
                return False
        return True

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
    number_of_players = countPlayers()
    # check for even number of players
    if number_of_players % 2 != 0:
        print "Odd number of players"
        exit()
    # players in match
    matched = []
    #this variable holds a list of players who already have been placed into a match
    previous_matched = []
    #matches
    matches = []
    # player standings
    player_standings = playerStandings()
    # create matches
    for i in player_standings:
			player = i[0]
			#only proceed if this player has not been put in a match
			if player not in previous_matched:
				# find a match for player
				for other in player_standings:
                                	#name the OTHER player
					other_player = other[0]
					#check if this_player and other_player can be matched
					if playerCheck(player,other_player) and other_player not in previous_matched:
						matches.append((
						player,
						i[1],
						other_player,
						other[1]
						))
						previous_matched.append(player)
						previous_matched.append(other_player)
						break
    return matches
