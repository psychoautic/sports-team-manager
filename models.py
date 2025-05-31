import random
from database import Database, DatabaseError

db = Database()

### Start by defining Classes

class Player:
    # Updated positions with more specific roles
    POSITIONS = [
        "GK",  # Goalkeeper
        # Defense
        "RB", "RCB", "CB", "LCB", "LB",  
        # Midfield
        "RDM", "CDM", "LDM",  # Defensive midfielders
        "RM", "RCM", "CM", "LCM", "LM",  # Central midfielders
        "RAM", "CAM", "LAM",  # Attacking midfielders
        # Attack
        "RW", "RS", "ST", "LS", "LW"  # Forwards
    ]
    
    def __init__(self, name, number, position):
        if not name or not isinstance(name, str):
            raise ValueError("Player name must be a non-empty string")
            
        if not isinstance(number, int) or number < 1 or number > 99:
            raise ValueError("Player number must be between 1 and 99")
            
        if position not in self.POSITIONS:
            raise ValueError(f"Invalid position. Must be one of {self.POSITIONS}")
            
        self.name = name
        self.number = number
        self.position = position
        self.id = None  # Database ID
        self.stats = {
            "goals": 0,
            "assists": 0,
            "games_played": 0
        }

    @classmethod
    def from_db_row(cls, row, team=None):
        # row format: id, name, number, position, goals, assists, games_played
        player = cls(
            name=row[1],
            number=row[2],
            position=row[3]
        )
        player.id = row[0]
        player.stats = {
            "goals": row[4] if row[4] is not None else 0,
            "assists": row[5] if row[5] is not None else 0,
            "games_played": row[6] if row[6] is not None else 0,
        }
        return player

    def update_stats(self, goals=0, assists=0):
        self.stats["goals"] += goals
        self.stats["assists"] += assists
        self.stats["games_played"] += 1

class Team:
    FORMATIONS = {
        "4-4-2": ["LB", "LCB", "RCB", "RB", "LM", "LCM", "RCM", "RM", "LS", "RS"],
        "4-3-3": ["LB", "LCB", "RCB", "RB", "LDM", "CDM", "RDM", "LW", "ST", "RW"],
        "3-5-2": ["LCB", "CB", "RCB", "LM", "LCM", "CDM", "RCM", "RM", "LS", "RS"],
        "4-2-3-1": ["LB", "LCB", "RCB", "RB", "LDM", "RDM", "LM", "CAM", "RM", "ST"],
        "4-5-1": ["LB", "LCB", "RCB", "RB", "LM", "LCM", "CDM", "RCM", "RM", "ST"]
    }

    def __init__(self, name, team_id=None, coach_name=None):
        if not name or not isinstance(name, str):
            raise ValueError("Team name must be a non-empty string")
            
        self.name = name
        self.coach = Coach(coach_name) if coach_name else None
        self.players = []
        self.id = team_id
        self.stats = {
            "games": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "GF": 0,
            "GA": 0   
        }
        self.current_formation = "4-4-2"  # Default formation
        self.lineup = {'GK': None}  # Initialize with empty goalkeeper
        self.lineup.update({pos: None for pos in self.FORMATIONS[self.current_formation]})
        
        if team_id is None:
            try:
                self.id = db.create_team(name, coach_name)
            except DatabaseError as e:
                raise DatabaseError(f"Failed to create team: {str(e)}")
        else:
            # If team_id is provided, load the lineup from database
            try:
                lineup_data = db.get_team_lineup(team_id)
                if lineup_data:
                    self.current_formation = lineup_data[0][0]
                    self.lineup = {'GK': None}
                    self.lineup.update({pos: None for pos in self.FORMATIONS[self.current_formation]})
                    
                    # Populate lineup with saved positions
                    for formation, lineup_pos, player_id, name, number, player_pos in lineup_data:
                        if player_id:  # Only set if player_id is not None
                            player = next((p for p in self.players if p.id == player_id), None)
                            if player:
                                self.lineup[lineup_pos] = player
            except DatabaseError:
                # If loading fails, keep default empty lineup
                pass

    def add_player(self, player):
        if not isinstance(player, Player):
            raise ValueError("Must be a Player instance")
            
        if any(p.number == player.number for p in self.players):
            raise ValueError(f"Number {player.number} is already taken")
            
        try:
            player_id = db.add_player(self.id, player.name, player.number, player.position)
            player.id = player_id
            self.players.append(player)
        except DatabaseError as e:
            raise DatabaseError(f"Failed to add player: {str(e)}")

    @classmethod
    def load_from_db(cls, team_name):
        try:
            team_data = db.get_team_by_name(team_name)
            if not team_data:
                return None
                
            team_id, name, coach_name = team_data
            team = cls(name, team_id=team_id, coach_name=coach_name)
            
            # Load players first so they're available for lineup assignment
            players_data = db.get_team_players(team_id)
            for player_data in players_data:
                player = Player.from_db_row(player_data)
                team.players.append(player)
                
            # Load lineup data
            lineup_data = db.get_team_lineup(team_id)
            if lineup_data:
                team.current_formation = lineup_data[0][0]
                team.lineup = {'GK': None}
                team.lineup.update({pos: None for pos in team.FORMATIONS[team.current_formation]})
                
                # Populate lineup with saved positions
                for formation, lineup_pos, player_id, name, number, player_pos in lineup_data:
                    if player_id:  # Only set if player_id is not None
                        player = next((p for p in team.players if p.id == player_id), None)
                        if player:
                            team.lineup[lineup_pos] = player
                
            # Load stats
            stats = db.get_team_stats(team_id)
            if stats:
                team.stats = {
                    "games": stats[0],
                    "wins": stats[1],
                    "draws": stats[2],
                    "losses": stats[3],
                    "GF": stats[4],
                    "GA": stats[5]
                }
                
            return team
        except DatabaseError as e:
            raise DatabaseError(f"Failed to load team: {str(e)}")

    @staticmethod
    def get_all_teams():
        try:
            teams = {}
            for team_data in db.get_all_teams():
                team_id, name, coach_name = team_data
                team = Team(name, team_id=team_id, coach_name=coach_name)
                
                # Load players first so they're available for lineup assignment
                players_data = db.get_team_players(team_id)
                for player_data in players_data:
                    player = Player.from_db_row(player_data)
                    team.players.append(player)
                    
                # Load lineup data
                lineup_data = db.get_team_lineup(team_id)
                if lineup_data:
                    team.current_formation = lineup_data[0][0]
                    team.lineup = {'GK': None}
                    team.lineup.update({pos: None for pos in team.FORMATIONS[team.current_formation]})
                    
                    # Populate lineup with saved positions
                    for formation, lineup_pos, player_id, name, number, player_pos in lineup_data:
                        if player_id:  # Only set if player_id is not None
                            player = next((p for p in team.players if p.id == player_id), None)
                            if player:
                                team.lineup[lineup_pos] = player
                
                # Load stats
                stats = db.get_team_stats(team_id)
                if stats:
                    team.stats = {
                        "games": stats[0],
                        "wins": stats[1],
                        "draws": stats[2],
                        "losses": stats[3],
                        "GF": stats[4],
                        "GA": stats[5]
                    }
                    
                teams[name] = team
            return teams
        except DatabaseError as e:
            raise DatabaseError(f"Failed to get teams: {str(e)}")

    def save_lineup(self):
        """Save current lineup to database"""
        try:
            # Save all positions including GK
            db.save_team_lineup(self.id, self.current_formation, self.lineup)
        except DatabaseError as e:
            raise DatabaseError(f"Failed to save lineup: {str(e)}")

    def set_formation(self, formation):
        if formation not in self.FORMATIONS:
            raise ValueError(f"Invalid formation. Must be one of {list(self.FORMATIONS.keys())}")
            
        self.current_formation = formation
        old_lineup = self.lineup.copy()
        # Keep goalkeeper and reset other positions
        self.lineup = {'GK': old_lineup.get('GK')}
        self.lineup.update({pos: None for pos in self.FORMATIONS[formation]})

    def assign_player_to_position(self, position, player):
        if position not in self.lineup:
            raise ValueError(f"Invalid position {position} for formation {self.current_formation}")
            
        if not isinstance(player, Player):
            raise ValueError("Must be a Player instance")
            
        # Remove player from any other position
        for pos in self.lineup:
            if self.lineup[pos] == player:
                self.lineup[pos] = None
                
        self.lineup[position] = player

    def remove_player_from_position(self, position):
        if position not in self.lineup:
            raise ValueError(f"Invalid position {position}")
            
        player = self.lineup[position]
        self.lineup[position] = None
        return player

    def update_stats(self, goals_for, goals_against):
        self.stats["games"] += 1
        self.stats["GF"] += goals_for
        self.stats["GA"] += goals_against
        
        if goals_for > goals_against:
            self.stats["wins"] += 1
        elif goals_for < goals_against:
            self.stats["losses"] += 1
        else:
            self.stats["draws"] += 1
            
        try:
            db.update_team_stats(
                self.id,
                games=1,
                wins=1 if goals_for > goals_against else 0,
                draws=1 if goals_for == goals_against else 0,
                losses=1 if goals_for < goals_against else 0,
                goals_for=goals_for,
                goals_against=goals_against
            )
        except DatabaseError as e:
            raise DatabaseError(f"Failed to update team stats: {str(e)}")

    # Team stats     
    def total_goals(self):
        return self.stats["GF"]

    def top_scorer(self):
        if not self.players:
            return None
        return max(self.players, key=lambda p: p.stats["goals"])
    
    def top_assister(self):
        if not self.players:
            return None
        return max(self.players, key=lambda p: p.stats["assists"])
    
    def avg_GFPG(self):
        if self.stats["games"] == 0:
            return 0
        return self.stats["GF"] / self.stats["games"]
    
    def avg_GAPG(self):
        if self.stats["games"] == 0:
            return 0
        return self.stats["GA"] / self.stats["games"]

class Match:
    def __init__(self, home_team, away_team):
        if not isinstance(home_team, Team) or not isinstance(away_team, Team):
            raise ValueError("Both teams must be Team instances")
        
        self.home_team = home_team
        self.away_team = away_team
        self.stadium = "Home Stadium"
        
    def match_simulate(self):
        # Basic match simulation logic
        home_attack_strength = len([p for p in self.home_team.players if p.position in ["ST", "LW", "RW", "CAM"]])
        home_midfield_strength = len([p for p in self.home_team.players if p.position in ["CM", "CDM", "LM", "RM"]])
        home_defense_strength = len([p for p in self.home_team.players if p.position in ["CB", "LB", "RB"]])
        
        # Simulate goals
        home_goals = random.randint(0, max(3, home_attack_strength + home_midfield_strength // 2))
        away_goals = random.randint(0, max(2, home_defense_strength // 2))  # Away team slightly disadvantaged
        
        # Simulate individual stats
        scorers = []
        assisters = []
        
        attackers = [p for p in self.home_team.players if p.position in ["ST", "LW", "RW", "CAM"]]
        midfielders = [p for p in self.home_team.players if p.position in ["CM", "CDM", "LM", "RM"]]
        
        for _ in range(home_goals):
            # 80% chance attacker scores, 20% chance midfielder scores
            if random.random() < 0.8 and attackers:
                scorer = random.choice(attackers)
            elif midfielders:
                scorer = random.choice(midfielders)
            else:
                continue
                
            # 70% chance of assist
            if random.random() < 0.7:
                # 60% chance midfielder assists, 40% chance attacker assists
                if random.random() < 0.6 and midfielders:
                    assister = random.choice([p for p in midfielders if p != scorer])
                elif attackers:
                    assister = random.choice([p for p in attackers if p != scorer])
                else:
                    assister = None
                    
                if assister:
                    assister.update_stats(assists=1)
            
            scorer.update_stats(goals=1)
        
        # Update team stats
        self.home_team.update_stats(home_goals, away_goals)
        self.away_team.update_stats(away_goals, home_goals)
        
        # Update goalkeeper clean sheet
        goalkeeper = next((p for p in self.home_team.players if p.position == "GK"), None)
        if goalkeeper and away_goals == 0:
            goalkeeper.update_stats(clean_sheet=True)
        
        return home_goals, away_goals

class Coach:
    def __init__(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Coach name must be a non-empty string")
        self.name = name

    def hire(self, team):
        self.team = team
        team.coach = self
    
    def fire(self):
        if self.team:
            self.team.coach = None
            self.team = None
        else:
            raise ValueError("Coach is not currently hired by any team.")