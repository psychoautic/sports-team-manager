import random

### Start by defining Classes

class Player:
    def __init__(self, name, number, position, team=None, attributes = None):
        self.name = name
        self.number = number
        self.position = position
        self.team = team
        self.attributes = attributes if attributes is not None else {}
        self.stats = {
            "goals": 0,
            "assists": 0,
            "Games_Played": 0
        }

class Team:
    FORMATIONS = {
        "4-4-2": ["GK", "RB", "CB1", "CB2", "LB", "RM", "CM1", "CM2", "LM", "ST1", "ST2"],
        "4-3-3": ["GK", "RB", "CB1", "CB2", "LB", "CM1", "CM2", "CAM", "RW", "LW", "ST"],
        "3-5-2": ["GK", "CB1", "CB2", "CB3", "LM", "RM", "CM1", "CM2", "CAM", "ST1", "ST2"],
        "5-3-2": ["GK", "CB1", "CB2", "CB3", "RB", "LB", "CM1", "CM2", "CAM", "ST1", "ST2"],
        "2-5-3": ["GK", "CB1", "CB2", "LM", "RM", "CM1", "CM2", "CAM", "ST1", "ST2", "ST3"]
    }

    def __init__(self, name):
        self.name = name
        self.players = []
        self.lineup = {}
        self.substitutes = []
        self.history = []
        self.formation = None
        self.stats = {
            "games": 0,
            "GF": 0,
            "GA": 0
        }

    def add_player(self, player):
        self.players.append(player)
        player.team = self
        self.substitutes.append(player)

    # Formation, Lineup and Player Management
    def set_formation(self, formation):
        self.formation = formation
        self.lineup = {position: None for position in self.FORMATIONS[formation]}
        self.substitutes = self.players[:]

    def assign_player_to_position(self, position, player):
        self.lineup[position] = player
        if player in self.substitutes:
            self.substitutes.remove(player)

    def remove_player_from_position(self, position):
        player = self.lineup[position]
        self.lineup[position] = None
        if player and player not in self.substitutes:
            self.substitutes.append(player)
        return player

        
    # Team stats     
    def total_goals(self):
        return sum(player.stats['goals'] for player in self.players)

    def top_scorer(self):
        return max(self.players, key=lambda p: p.stats['goals'], default=None)
    
    def top_assister(self):
        return max(self.players, key=lambda p: p.stats['assists'], default=None)
    
    def avg_GFPG(self):
        if self.stats["games"] == 0:
            return 0
        return self.stats["GF"] / self.stats["games"]
    
    def avg_GAPG(self):
        if self.stats["games"] == 0:
            return 0
        return self.stats["GA"] / self.stats["games"]

        
class Match:
    def __init__(self, myteam, opponent):
        self.myteam = myteam
        self.opponent = opponent
        self.date = None
        self.stadium = None
        self.result = None
    

    def match_simulate(self):
        print(f"Simulating match between {self.myteam.name} and {self.opponent.name}")
        
        # Simulation & Result
        myteam_score = random.randint(0, 5)
        opponent_score = random.randint(0, 5)
        self.result = (myteam_score, opponent_score)

        # Update match stats & result to team and players
        self.myteam.stats["games"] += 1

        for goal in range(myteam_score):
            self.myteam.stats["GF"] += 1
        for goal in range(opponent_score):
            self.myteam.stats["GA"] += 1
        for player in self.myteam.lineup:
            player.stats["Games_Played"] += 1
        
        for i in range(myteam_score):
            scorer = random.choice(self.myteam.lineup)
            scorer.stats["goals"] += 1

            assister_candidates = [p for p in self.myteam.lineup if p != scorer]
            assister = random.choice(assister_candidates)
            assister.stats["assists"] += 1

        self.myteam.history.append({
            "opponent": self.opponent.name,
            "result": self.result,
            "date": self.date,
            "stadium": self.stadium
        })





class Coach:
    def __init__(self, name, team=None):
        self.name = name
        self.team = team

    def hire(self, team):
            self.team = team
            team.coach = self
    
    def fire(self):
        if self.team:
            self.team.coach = None
            self.team = None
        else:
            raise ValueError("Coach is not currently hired by any team.")