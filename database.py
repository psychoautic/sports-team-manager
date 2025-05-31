import sqlite3
from contextlib import contextmanager

class DatabaseError(Exception):
    pass

class Database:
    def __init__(self, db_name="team_manager.db"):
        self.db_name = db_name
        self.setup_database()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def setup_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create Teams table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    coach_name TEXT
                )
            ''')

            # Create Players table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id INTEGER,
                    name TEXT NOT NULL,
                    number INTEGER NOT NULL,
                    position TEXT NOT NULL,
                    goals INTEGER DEFAULT 0,
                    assists INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    FOREIGN KEY (team_id) REFERENCES teams (id),
                    UNIQUE(team_id, number)
                )
            ''')

            # Create Team Stats table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id INTEGER,
                    games INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    draws INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    goals_for INTEGER DEFAULT 0,
                    goals_against INTEGER DEFAULT 0,
                    FOREIGN KEY (team_id) REFERENCES teams (id)
                )
            ''')

            # Create Team Lineup table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_lineups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id INTEGER NOT NULL,
                    formation TEXT NOT NULL,
                    position TEXT NOT NULL,
                    player_id INTEGER,
                    FOREIGN KEY (team_id) REFERENCES teams (id),
                    FOREIGN KEY (player_id) REFERENCES players (id),
                    UNIQUE(team_id, position)
                )
            ''')

            conn.commit()

    def create_team(self, team_name, coach_name=None):
        if not team_name or not team_name.strip():
            raise DatabaseError("Team name cannot be empty")
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT id FROM teams WHERE name = ?', (team_name,))
                if cursor.fetchone():
                    raise DatabaseError(f"Team '{team_name}' already exists")
                
                cursor.execute('INSERT INTO teams (name, coach_name) VALUES (?, ?)', (team_name, coach_name))
                team_id = cursor.lastrowid
                
                cursor.execute('INSERT INTO team_stats (team_id) VALUES (?)', (team_id,))
                conn.commit()
                return team_id
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Failed to create team: {str(e)}")

    def add_player(self, team_id, name, number, position):
        if not name or not name.strip():
            raise DatabaseError("Player name cannot be empty")
        if not isinstance(number, int) or number < 1 or number > 99:
            raise DatabaseError("Player number must be between 1 and 99")
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT id FROM players WHERE team_id = ? AND number = ?', (team_id, number))
                if cursor.fetchone():
                    raise DatabaseError(f"Number {number} is already taken in this team")
                
                cursor.execute('''
                    INSERT INTO players (team_id, name, number, position)
                    VALUES (?, ?, ?, ?)
                ''', (team_id, name, number, position))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Failed to add player: {str(e)}")

    def update_team(self, team_id, name=None, coach_name=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if name:
                    cursor.execute('SELECT id FROM teams WHERE name = ? AND id != ?', (name, team_id))
                    if cursor.fetchone():
                        raise DatabaseError(f"Team name '{name}' is already taken")
                    cursor.execute('UPDATE teams SET name = ? WHERE id = ?', (name, team_id))
                
                if coach_name is not None:  # Allow empty string for coach_name
                    cursor.execute('UPDATE teams SET coach_name = ? WHERE id = ?', (coach_name, team_id))
                
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Failed to update team: {str(e)}")

    def update_player(self, player_id, name=None, number=None, position=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if number:
                    # Get player's team_id
                    cursor.execute('SELECT team_id FROM players WHERE id = ?', (player_id,))
                    team_id = cursor.fetchone()[0]
                    # Check if number is taken by another player
                    cursor.execute('''
                        SELECT id FROM players 
                        WHERE team_id = ? AND number = ? AND id != ?
                    ''', (team_id, number, player_id))
                    if cursor.fetchone():
                        raise DatabaseError(f"Number {number} is already taken in this team")
                
                updates = []
                params = []
                if name:
                    updates.append("name = ?")
                    params.append(name)
                if number:
                    updates.append("number = ?")
                    params.append(number)
                if position:
                    updates.append("position = ?")
                    params.append(position)
                
                if updates:
                    params.append(player_id)
                    cursor.execute(f'''
                        UPDATE players 
                        SET {", ".join(updates)}
                        WHERE id = ?
                    ''', params)
                    conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Failed to update player: {str(e)}")

    def get_all_teams(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, coach_name FROM teams')
            return cursor.fetchall()

    def get_team_by_name(self, team_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, coach_name FROM teams WHERE name = ?', (team_name,))
            return cursor.fetchone()

    def get_team_players(self, team_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, number, position, goals, assists, games_played
                FROM players
                WHERE team_id = ?
                ORDER BY number
            ''', (team_id,))
            return cursor.fetchall()

    def get_team_stats(self, team_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT games, wins, draws, losses, goals_for, goals_against
                FROM team_stats
                WHERE team_id = ?
            ''', (team_id,))
            result = cursor.fetchone()
            if not result:
                # Initialize stats if not found
                cursor.execute('''
                    INSERT INTO team_stats (team_id, games, wins, draws, losses, goals_for, goals_against)
                    VALUES (?, 0, 0, 0, 0, 0, 0)
                ''', (team_id,))
                conn.commit()
                return (0, 0, 0, 0, 0, 0)
            return result

    def delete_team(self, team_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Delete all related records first
                cursor.execute('DELETE FROM players WHERE team_id = ?', (team_id,))
                cursor.execute('DELETE FROM team_stats WHERE team_id = ?', (team_id,))
                cursor.execute('DELETE FROM teams WHERE id = ?', (team_id,))
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Failed to delete team: {str(e)}")

    def update_team_stats(self, team_id, games=0, wins=0, draws=0, losses=0, goals_for=0, goals_against=0):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    UPDATE team_stats 
                    SET games = games + ?,
                        wins = wins + ?,
                        draws = draws + ?,
                        losses = losses + ?,
                        goals_for = goals_for + ?,
                        goals_against = goals_against + ?
                    WHERE team_id = ?
                ''', (games, wins, draws, losses, goals_for, goals_against, team_id))
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Could not update team stats: {str(e)}")

    def update_player_stats(self, player_id, goals=0, assists=0, games_played=0):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    UPDATE players 
                    SET goals = goals + ?,
                        assists = assists + ?,
                        games_played = games_played + ?
                    WHERE id = ?
                ''', (goals, assists, games_played, player_id))
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Could not update player stats: {str(e)}")

    def save_team_lineup(self, team_id, formation, lineup_dict):
        """Save team's current lineup to database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # First clear existing lineup
                cursor.execute('DELETE FROM team_lineups WHERE team_id = ?', (team_id,))
                
                # Insert new lineup - save all positions, even empty ones
                for position in lineup_dict:
                    player = lineup_dict[position]
                    cursor.execute('''
                        INSERT INTO team_lineups (team_id, formation, position, player_id)
                        VALUES (?, ?, ?, ?)
                    ''', (team_id, formation, position, player.id if player else None))
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"Failed to save lineup: {str(e)}")

    def get_team_lineup(self, team_id):
        """Get team's saved lineup from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT formation, team_lineups.position as lineup_position, 
                       players.id, players.name, players.number, players.position as player_position
                FROM team_lineups
                LEFT JOIN players ON team_lineups.player_id = players.id
                WHERE team_lineups.team_id = ?
            ''', (team_id,))
            return cursor.fetchall() 