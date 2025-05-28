from typing import List, Optional, Dict


from models.player import Player
from models.coach import Coach


class Team:
    def __init__(self, name: str, coach: Optional['Coach'] = None, players: Optional[List['Player']] = None):
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
            player.team = self  ### This line sets the team attribute of the player to this team

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
            'coach': self.coach,
            'players': [player.name for player in self.players]
        }


    ### Lineup management methods
    def select_lineup(self, lineup: List[Player], substitutes: List[Player] = None):
        if len(lineup) > 11:
            raise ValueError("Lineup cannot have more than 11 players.")
        if not all(player in self.players for player in lineup):
            raise ValueError("All lineup players must be in the team roster.")
        self.lineup = lineup
        self.substitutes = substitutes if substitutes else []

    def add_to_lineup(self, player: Player):
        if not hasattr(self, 'lineup'):
            self.lineup = []
        if len(self.lineup) >= 11:
            raise ValueError("Lineup cannot have more than 11 players.")
        if player not in self.players:
            raise ValueError("Player must be in the team roster.")
        if player in self.lineup:
            raise ValueError("Player is already in the lineup.")
        self.lineup.append(player)

    def remove_from_lineup(self, player: Player):
        if not hasattr(self, 'lineup') or player not in self.lineup:
            raise ValueError("Player is not in the lineup.")
        self.lineup.remove(player)