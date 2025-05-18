from typing import List, Optional, Dict
import sqlite3
import random
import json

conn = sqlite3.connect('football_game.db')
cursor = conn.cursor()


class Team:
    def __init__(self, name: str, coach: Optional['Coach'] = None, players: Optional[List['Player']] = None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        self.name = name
        self.coach = coach if coach is not None else "Unknown"
        self.players = []

        cursor.execute("INSERT INTO teams (name, president, coach_id) VALUES (?, ?, ?)", (self.name, self.president, self.coach))

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

        # Random score simulation (placeholder)
        self.result[self.team_a.name] = random.randint(0, 5)
        self.result[self.team_b.name] = random.randint(0, 5)

        print(f"Match ended with score: {self.team_a.name} {self.result[self.team_a.name]} - {self.result[self.team_b.name]} {self.team_b.name}")

        if self.result[self.team_a.name] > self.result[self.team_b.name]:
            winner = self.team_a.name
        elif self.result[self.team_b.name] > self.result[self.team_a.name]:
            winner = self.team_b.name
        else:
            winner = "Draw"
        
        print(f"Result: {winner}")


    

class tournament:
    TOURNAMENT_TYPES = ['League', 'Knockout', 'Friendly']
    def __init__(self, name: str, tournament_type: str, teams: List['Team'] = None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if tournament_type not in self.TOURNAMENT_TYPES:
            raise ValueError(f"Invalid tournament type. Must be one of {self.TOURNAMENT_TYPES}")

        self.name: str = name
        self.tournament_type: str = tournament_type
        self.teams: List['Team'] = teams if teams else []


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






