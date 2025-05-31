from database import Database  # Update this to match your filename
import random

db = Database()

teams_data = [
    {
        "name": "Real Madrid",
        "coach": "Xabi Alonso",
        "players": [
            ("Thibaut Courtois", 1, "GK"),
            ("Éder Militão", 3, "RCB"),
            ("Antonio Rüdiger", 22, "LCB"),
            ("Trent Alexander-Arnold", 66, "RB"),
            ("Ferland Mendy", 23, "LB"),
            ("Aurélien Tchouaméni", 18, "CDM"),
            ("Eduardo Camavinga", 12, "LCM"),
            ("Federico Valverde", 15, "RCM"),
            ("Jude Bellingham", 5, "CAM"),
            ("Vinícius Júnior", 7, "LW"),
            ("Rodrygo", 11, "RW"),
            ("Kylian Mbappé", 10, "ST"),
            ("Endrick", 9, "RS"),
            ("Dean Huijsen", 24, "CB"),
            ("Jesús Vallejo", 6, "LCB"),
        ],
    },
    {
        "name": "Paris Saint-Germain",
        "coach": "Luis Enrique",
        "players": [
            ("Gianluigi Donnarumma", 99, "GK"),
            ("Marquinhos", 5, "RCB"),
            ("William Pacho", 4, "LCB"),
            ("Achraf Hakimi", 2, "RB"),
            ("Nuno Mendes", 25, "LB"),
            ("Vitinha", 17, "RCM"),
            ("Fabián Ruiz", 8, "LCM"),
            ("João Neves", 27, "CDM"),
            ("Ousmane Dembélé", 10, "RW"),
            ("Khvicha Kvaratskhelia", 77, "LW"),
            ("Bradley Barcola", 29, "ST"),
            ("Desire Doue", 31, "CAM"),
            ("Presnel Kimpembe", 3, "CB"),
            ("Marco Asensio", 11, "RAM"),
            ("Randal Kolo Muani", 23, "RS"),
        ],
    },
    {
        "name": "Bayern Munich",
        "coach": "Thomas Tuchel",
        "players": [
            ("Manuel Neuer", 1, "GK"),
            ("Jonathan Tah", 4, "RCB"),
            ("Dayot Upamecano", 2, "LCB"),
            ("Alphonso Davies", 19, "LB"),
            ("Joshua Kimmich", 6, "RCM"),
            ("Leon Goretzka", 8, "LCM"),
            ("Jamal Musiala", 42, "CAM"),
            ("Leroy Sané", 10, "RW"),
            ("Kingsley Coman", 11, "LW"),
            ("Serge Gnabry", 7, "RS"),
            ("Harry Kane", 9, "ST"),
            ("Thomas Müller", 25, "RAM"),
            ("Noussair Mazraoui", 40, "RB"),
            ("Matthijs de Ligt", 5, "CB"),
            ("Eric Maxim Choupo-Moting", 13, "LS"),
        ],
    },
    {
        "name": "Manchester City",
        "coach": "Pep Guardiola",
        "players": [
            ("Ederson", 31, "GK"),
            ("Rúben Dias", 3, "RCB"),
            ("Joško Gvardiol", 24, "LCB"),
            ("John Stones", 5, "CB"),
            ("Kyle Walker", 2, "RB"),
            ("Rodri", 16, "CDM"),
            ("Kevin De Bruyne", 17, "RCM"),
            ("Bernardo Silva", 20, "CAM"),
            ("Phil Foden", 47, "LAM"),
            ("Jack Grealish", 10, "LW"),
            ("Jérémy Doku", 11, "RW"),
            ("Erling Haaland", 9, "ST"),
            ("Mateo Kovačić", 8, "LCM"),
            ("Matheus Nunes", 27, "RDM"),
            ("Oscar Bobb", 52, "RS"),
        ],
    },
]

# First create all teams and store their IDs
team_ids = {}
for team in teams_data:
    try:
        team_id = db.create_team(team["name"], coach_name=team["coach"])
        team_ids[team["name"]] = team_id
        for name, number, position in team["players"]:
            db.add_player(team_id, name, number, position)
        print(f"✅ Created team: {team['name']}")
    except Exception as e:
        print(f"⚠️ Error creating team {team['name']}: {e}")

# Simulate matches between teams
print("\nSimulating matches between teams...")
# Each team plays against every other team once
teams = list(team_ids.keys())
for i in range(len(teams)):
    for j in range(i + 1, len(teams)):
        home_team = teams[i]
        away_team = teams[j]
        
        # Simulate a match with random scores (0-4 goals per team)
        home_score = random.randint(0, 4)
        away_score = random.randint(0, 4)
        
        try:
            # Update home team stats
            if home_score > away_score:
                db.update_team_stats(team_ids[home_team], games=1, wins=1, goals_for=home_score, goals_against=away_score)
                db.update_team_stats(team_ids[away_team], games=1, losses=1, goals_for=away_score, goals_against=home_score)
            elif home_score < away_score:
                db.update_team_stats(team_ids[home_team], games=1, losses=1, goals_for=home_score, goals_against=away_score)
                db.update_team_stats(team_ids[away_team], games=1, wins=1, goals_for=away_score, goals_against=home_score)
            else:
                db.update_team_stats(team_ids[home_team], games=1, draws=1, goals_for=home_score, goals_against=away_score)
                db.update_team_stats(team_ids[away_team], games=1, draws=1, goals_for=away_score, goals_against=home_score)
            
            print(f"✅ Match result: {home_team} {home_score} - {away_score} {away_team}")
        except Exception as e:
            print(f"⚠️ Error recording match result: {e}")

print("\nPopulation completed!")
