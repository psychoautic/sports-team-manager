
team1 = Team("Red Warriors")
team2 = Team("Blue Hawks")

players1 = [Player(f"RW_Player{i}", "ST", i) for i in range(1, 12)]
players2 = [Player(f"BH_Player{i}", "CB", i+11) for i in range(1, 12)]

for p in players1:
    team1.add_player(p)
for p in players2:
    team2.add_player(p)

team1.select_lineup(players1[:11])
team2.select_lineup(players2[:11])

match = Match(team1, team2, date="2025-05-28", stadium="National Stadium")
match.match_simulate()



