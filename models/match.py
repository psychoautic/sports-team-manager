from typing import List, Optional, Dict
from models.team import Team
import random


class Match:
    def __init__(self, team_a: 'Team', team_b: 'Team', date: str = None, stadium: str = None, result: dict = None):

        if not isinstance(team_a, Team) or not isinstance(team_b, Team):
            raise TypeError("team_a and team_b must be instances of Team class")
        if team_a == team_b:
            raise ValueError("A team cannot play against itself")
        if not isinstance(date, str):
            raise TypeError("Date must be a string")
        if not isinstance(stadium, str):
            raise TypeError("Stadium must be a string")
         
        self.team_a: 'Team' = team_a
        self.team_b: 'Team' = team_b
        self.date: str = date
        self.stadium: str = stadium
        self.result: dict = result if result else {self.team_a.name : 0, self.team_b.name : 0}

    def match_info(self):
        return {
            'team_a': self.team_a.name,
            'team_b': self.team_b.name,
            'date': self.date,
            'stadium': self.stadium,
            'result': self.result
        }
    
    def match_simulate(self):
        print(f"Match between {self.team_a.name} and {self.team_b.name} has started at {self.stadium} on {self.date}")

        # Random score simulation
        self.result[self.team_a.name] = random.randint(0, 5)
        self.result[self.team_b.name] = random.randint(0, 5)

        print(f"Match ended with score: {self.team_a.name} {self.result[self.team_a.name]} - {self.result[self.team_b.name]} {self.team_b.name}")

        # Assign goals and assists randomly
        player_stats = {}
        for team in [self.team_a, self.team_b]:
            lineup = getattr(team, 'lineup', [])
            goals = self.result[team.name]
            for player in lineup:
                player_stats[player] = {'goals': 0, 'assists': 0, 'games_played': 1}
            for _ in range(goals):
                scorer = random.choice(lineup)
                assister_candidates = [p for p in lineup if p != scorer]
                assister = random.choice(assister_candidates) if assister_candidates else None
                player_stats[scorer]['goals'] += 1
                if assister:
                    player_stats[assister]['assists'] += 1

        self.record_player_stats(player_stats)

        if self.result[self.team_a.name] > self.result[self.team_b.name]:
            winner = self.team_a.name
        elif self.result[self.team_b.name] > self.result[self.team_a.name]:
            winner = self.team_b.name
        else:
            winner = "Draw"
        print(f"Result: {winner}")

    def get_playing_players(self):
        return self.team_a.lineup + self.team_b.lineup

    def record_player_stats(self, player_stats: dict):
        from models.game_stat import GameStat
        for player, stats in player_stats.items():
            gs = GameStat(
                opponent=(self.team_b if player in self.team_a.lineup else self.team_a).name,
                goals=stats.get('goals', 0),
                assists=stats.get('assists', 0),
                games_played=stats.get('games_played', 1)
            )
            player.stats.append(gs)

