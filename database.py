import sqlite3
import json

conn = sqlite3.connect('football_manager.db')
cur = conn.cursor()



# Creating our Football Manager database Tables
# teams, players, coaches, matches and tournaments

cur.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    team_id INTEGER,
    position TEXT,
    attributes TEXT,
    FOREIGN KEY (team_id) REFERENCES teams (id)
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    president TEXT,
    coach_id INTEGER,
    FOREIGN KEY (coach_id) REFERENCES coaches (id)
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS coaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    experience INTEGER
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1_id INTEGER,
    team2_id INTEGER,
    score TEXT,
    date TEXT,
    FOREIGN KEY (team1_id) REFERENCES teams (id),
    FOREIGN KEY (team2_id) REFERENCES teams (id)
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT
)''')


def connect_db():
    return sqlite3.connect('football_game.db')

def save_player(conn, player):
    
    cur.execute(
        "INSERT INTO players (name, team_id, position, attributes) VALUES (?, ?, ?, ?)",
        (player.name, player.team.id if player.team else None, player.position, json.dumps(player.attributes))
    )
    conn.commit()
