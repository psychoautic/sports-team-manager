from typing import List, Optional, Dict

class Team:
    def __init__(self, name: str, president: str = None, coach: Optional['Coach'] = None, players: Optional[List['Player']] = None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        self.name = name
        self.coach = coach if coach is not None else "Unknown"
        self.players = []

        if players is not None:
            if not isinstance(players, list) or not all(isinstance(p, Player) for p in players):
                raise TypeError("Players must be a list of Player objects")
            for player in players:
                self.add_player(player)

    def add_player(self, player: 'Player'):
        if not isinstance(player, Player):
            raise TypeError("Player must be an instance of Player class")
        if player not in self.players:
            self.players.append(player)
            player.team = self  # Set back-reference

    def remove_player(self, player: 'Player'):
        if not isinstance(player, Player):
            raise TypeError("Player must be an instance of Player class")
        if player in self.players:
            self.players.remove(player)
            player.team = None
        else:
            print(f"Player {player.name} not found in team {self.name}")

    def team_info(self):
        return {
            'name': self.name,
            'president': self.president,
            'coach': self.coach,
            'players': [player.name for player in self.players]
        }


    
class Player:
    ALLOWED_POSITIONS = {'GK', 'CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LM', 'RM', 'LW', 'RW', 'ST'}
    ALLOWED_ATTRIBUTES = {'speed', 'stamina', 'strength', 'agility', 'passing', 'shooting', 'defending'}

    def __init__(self, name: str, position: str = None, number: int = None, team: Optional['Team'] = None, attributes: Optional[Dict[str, int]] = None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if position is not None and position not in self.ALLOWED_POSITIONS:
            raise ValueError(f"Position must be one of {self.ALLOWED_POSITIONS}")
        if number is not None and not isinstance(number, int):
            raise TypeError("Number must be an integer")
        
        self.name= name
        self.position = position
        self.number= number
        self.team = None
        self.attributes = {attr: 0 for attr in Player.ALLOWED_ATTRIBUTES}


        if attributes:
            for attr, value in attributes.items():
                if attr not in Player.ALLOWED_ATTRIBUTES:
                    raise ValueError(f"Invalid attribute '{attr}'. Must be one of {Player.ALLOWED_ATTRIBUTES}")
                if not isinstance(value, int):
                    raise TypeError(f"Value for '{attr}' must be an integer")
                if value < 0 or value > 100:
                    raise ValueError("Attribute value must be between 0 and 100")
                self.attributes[attr] = value

        if team:
            self.change_team(team)


    def update_attributes(self, attribute: str, value: int):
        if attribute not in Player.ALLOWED_ATTRIBUTES:
            raise ValueError(f"Invalid attribute '{attribute}'. Must be one of {Player.ALLOWED_ATTRIBUTES}")
        if not isinstance(value, int):
            raise TypeError("Attribute value must be an integer")
        if value < 0 or value > 100:
            raise ValueError("Attribute value must be between 0 and 100")
        
        self.attributes[attribute] = value

    def  change_team(self, new_team: 'Team'):
        if self.team:
            self.team.remove_player(self)
        new_team.add_player(self)
        
class Coach:
    ALLOWED_ATTRIBUTES = ["tactics", "motivation", "discipline", "adaptability", "leadership", "training"]

    def __init__(self, name: str, attributes: Optional[Dict[str, int]] = None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        self.name = name
        self.attributes = {attr: 0 for attr in Coach.ALLOWED_ATTRIBUTES}

        if attributes:
            for attr, value in attributes.items():
                if attr not in Coach.ALLOWED_ATTRIBUTES:
                    raise ValueError(f"Invalid attribute '{attr}'. Must be one of {Coach.ALLOWED_ATTRIBUTES}")
                if not isinstance(value, int) or not (0 <= value <= 100):
                    raise ValueError("Attribute values must be integers between 0 and 100")
                self.attributes[attr] = value


class Match:
    def __init__(self, team_a: 'Team', team_b: 'Team', date: str = None, location: str = None, result: dict = None):
        self.team_a: 'Team' = team_a
        self.team_b: 'Team' = team_b
        self.date: str = date
        self.location: str = location
        self.result: dict = result if result else {'team_a': 0, 'team_b': 0}


    def update_result(self, team_a_score: int, team_b_score: int):
        self.result['team_a'] = team_a_score
        self.result['team_b'] = team_b_score

class League:
    def __init__(self, name: str, teams: List['Team'] = None):
        self.name: str = name
        self.teams: List['Team'] = teams if teams else []



#TESTING
team1 = Team("Alpha")
team2 = Team("Beta")

player1 = Player(name="Alex", position="ST")
team1.add_player(player1)

player1.change_team(team2)  # This should call remove_player from team1

print(team1.players)  # Should not contain player1
print(team2.players)  # Should contain player1
