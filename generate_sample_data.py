"""Generates a FICTIONAL sample dataset (teams, players, stats) so the project
runs out of the box. Swap the CSVs in /data for real data when you have it."""
import random
import pandas as pd

random.seed(42)

TEAMS = ["Riverside FC", "Northgate United", "Harbor City", "Sunvale Athletic", "Ironwood Rovers"]
FIRST = ["Alex", "Marco", "Luis", "Sam", "Diego", "Jonas", "Ravi", "Tom", "Omar", "Felix",
         "Kai", "Mateo", "Leo", "Ivan", "Noah", "Eli", "Hugo", "Yusuf", "Ben", "Carlos"]
LAST = ["Silva", "Novak", "Reyes", "Khan", "Dubois", "Meyer", "Costa", "Ito", "Lopez", "Berg",
        "Moreau", "Santos", "Petrov", "Walsh", "Ortiz", "Haas", "Rossi", "Lind", "Duarte", "Okafor"]
SEASONS = [2022, 2023, 2024, 2025]
SQUAD = ["GK"] + ["DF"] * 3 + ["MF"] * 3 + ["FW"] * 3  # 10 players per team

# (goals/90, assists/90, shots/90) baselines by position
RATES = {"GK": (0.0, 0.01, 0.0), "DF": (0.05, 0.07, 0.6),
         "MF": (0.15, 0.20, 1.5), "FW": (0.50, 0.25, 3.0)}

teams = pd.DataFrame({"team_id": range(1, len(TEAMS) + 1), "name": TEAMS})

players, stats, pid = [], [], 1
used = set()
for team_id in teams["team_id"]:
    for pos in SQUAD:
        while True:
            name = f"{random.choice(FIRST)} {random.choice(LAST)}"
            if name not in used:
                used.add(name)
                break
        players.append({"player_id": pid, "name": name, "position": pos, "team_id": team_id})
        skill = random.uniform(0.7, 1.4)
        for season in SEASONS:
            skill *= random.uniform(0.92, 1.12)  # gradual improvement/decline
            matches = random.randint(20, 34)
            minutes = int(matches * random.uniform(55, 90))
            n90 = minutes / 90
            g, a, s = RATES[pos]
            shots = int(n90 * s * skill * random.uniform(0.8, 1.2))
            sot = int(shots * random.uniform(0.3, 0.5))
            goals = min(sot, int(round(n90 * g * skill * random.uniform(0.6, 1.4))))
            assists = int(round(n90 * a * skill * random.uniform(0.6, 1.4)))
            stats.append({"player_id": pid, "season": season, "matches_played": matches,
                          "minutes": minutes, "goals": goals, "assists": assists,
                          "shots": shots, "shots_on_target": sot,
                          "yellow_cards": random.randint(0, 9)})
        pid += 1

teams.to_csv("data/teams.csv", index=False)
pd.DataFrame(players).to_csv("data/players.csv", index=False)
pd.DataFrame(stats).to_csv("data/player_stats.csv", index=False)
print(f"Wrote {len(teams)} teams, {len(players)} players, {len(stats)} stat rows to /data")
