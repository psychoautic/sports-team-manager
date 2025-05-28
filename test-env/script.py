# Example test script for your sports team manager

from models.player import Player
from models.team import Team
from models.match import Match

# Create players
players_a = [Player(name=f"PlayerA{i+1}", position="ST", number=i+1) for i in range(11)]
players_b = [Player(name=f"PlayerB{i+1}", position="ST", number=i+1) for i in range(11)]

# Create teams
team_a = Team(name="Team A", players=players_a)
team_b = Team(name="Team B", players=players_b)

# Select lineups
team_a.select_lineup(lineup=players_a)
team_b.select_lineup(lineup=players_b)

# Create and simulate a match
match = Match(team_a=team_a, team_b=team_b, date="2025-05-28", stadium="Main Stadium")
match.match_simulate()

# Print player stats for Team A
print("\nTeam A Player Stats:")
for player in team_a.lineup:
    for stat in player.stats:
        print(f"{player.name}: Goals={stat.goals}, Assists={stat.assists}, Games Played={stat.games_played}, Opponent={stat.opponent}")

# Print player stats for Team B
print("\nTeam B Player Stats:")
for player in team_b.lineup:
    for stat in player.stats:
        print(f"{player.name}: Goals={stat.goals}, Assists={stat.assists}, Games Played={stat.games_played}, Opponent={stat.opponent}")