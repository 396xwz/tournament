# tournament
Swiss style tournament
Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
The game tournament will use the Swiss system for pairing up players in each round.

INSTALLATION    
        Linux: install from a repository        
USAGE   
        tournament.sql is the database schema   
        tournament.py is the Python module      
        tournament_test.py contains unit tests that will test the functions     
        
        Creating Your Database
        Before you can run your code or create your tables, you'll need to use the create database command in psql to create the database. Use the name tournament for your database.  
        Use the command \i tournament.sql to import the whole file into psql at once.
        
        run python tournament_test.py
