from models.match import Match
from models.team import Team
from typing import List



class Tournament:
    TOURNAMENT_TYPES = ['League', 'Knockout', 'Friendly']
    def __init__(self, name: str, tournament_type: str, teams: List['Team'] = None, matches: List[Match] = None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if tournament_type not in self.TOURNAMENT_TYPES:
            raise ValueError(f"Invalid tournament type. Must be one of {self.TOURNAMENT_TYPES}")

        self.name: str = name
        self.tournament_type: str = tournament_type
        self.teams: List['Team'] = teams if teams else []
        self.matches: List[Match] = []


    def simulate(self):
        print(f"\n--- Simulating {self.name} ({self.tournament_type}) ---")

        if self.tournament_type == 'League':
            self._simulate_league()
        elif self.tournament_type == 'Knockout':
            self._simulate_knockout()
        elif self.tournament_type == 'Friendly':
            self._simulate_friendly()

    def _simulate_league(self):
        self.generate_matches()
        standings = {team.name: {'points': 0, 'goals': 0} for team in self.teams}

        for match in self.matches:
            match.match_simulate()

            team_a = match.team_a.name
            team_b = match.team_b.name
            score_a = match.result[team_a]
            score_b = match.result[team_b]

            standings[team_a]['goals'] += score_a
            standings[team_b]['goals'] += score_b

            if score_a > score_b:
                standings[team_a]['points'] += 3
            elif score_b > score_a:
                standings[team_b]['points'] += 3
            else:
                standings[team_a]['points'] += 1
                standings[team_b]['points'] += 1

        print("\n🏁 Final League Standings:")
        sorted_standings = sorted(standings.items(), key=lambda x: (-x[1]['points'], -x[1]['goals']))
        for rank, (team, stats) in enumerate(sorted_standings, 1):
            print(f"{rank}. {team} - {stats['points']} pts, {stats['goals']} goals")

        print(f"\n🏆 Winner: {sorted_standings[0][0]}")

    def _simulate_knockout(self):
        import random
        current_round = 1
        teams = self.teams[:]
        round_number = 1

        while len(teams) > 1:
            print(f"\n--- Round {round_number} ---")
            round_matches = []
            random.shuffle(teams)
            next_round_teams = []

            while len(teams) >= 2:
                team_a = teams.pop()
                team_b = teams.pop()
                match = Match(team_a, team_b)
                match.match_simulate()

                winner = team_a if match.result[team_a.name] > match.result[team_b.name] else team_b
                print(f"🏅 {winner.name} advances")
                next_round_teams.append(winner)
                round_matches.append(match)

            self.matches.extend(round_matches)
            teams = next_round_teams
            round_number += 1

        print(f"\n🏆 Knockout Winner: {teams[0].name}")

    def _simulate_friendly(self):
        self.generate_matches()
        for match in self.matches:
            match.match_simulate()
        print(f"\n🏆 Friendly Match Winner: {match.result}")
