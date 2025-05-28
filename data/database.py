import sqlite3

connection = sqlite3.connect('FM.db')
cursor = connection.cursor()



### Table creation statements

cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    team_id INTEGER,
    position TEXT,
    attributes TEXT,
    FOREIGN KEY (team_id) REFERENCES teams (id)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    president TEXT,
    coach_id INTEGER,
    FOREIGN KEY (coach_id) REFERENCES coaches (id)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS coaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    experience INTEGER
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1_id INTEGER,
    team2_id INTEGER,
    score TEXT,
    date TEXT,
    FOREIGN KEY (team1_id) REFERENCES teams (id),
    FOREIGN KEY (team2_id) REFERENCES teams (id)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT
)''')
