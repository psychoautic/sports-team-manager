from typing import List, Optional, Dict
from models.team import Team
from models.game_stat import GameStat


class Player:
    ALLOWED_POSITIONS = {'GK', 'CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LM', 'RM', 'LW', 'RW', 'ST'}
    ALLOWED_ATTRIBUTES = {'speed', 'stamina', 'strength', 'agility', 'passing', 'shooting', 'defending'}

    def __init__(self, name: str, position: str = None, number: int = None, team: Optional['Team'] = None, attributes: Optional[Dict[str, int]] = None, stats: Optional[List[GameStat]] = None):
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
        self.stats = []
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