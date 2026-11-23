"""Soccer Analytics Dashboard - entry point.

Usage:
    python main.py                      # analyze CSV data in /data
    python main.py --init-db            # create tables + load CSVs into PostgreSQL
    python main.py --source postgres    # analyze data stored in PostgreSQL
    python main.py --season 2024        # pick a season (default: latest)
"""
import argparse

import pandas as pd

from src import analysis, visualize
from src.db import get_engine, init_db


def main():
    parser = argparse.ArgumentParser(description="Soccer Analytics Dashboard")
    parser.add_argument("--source", choices=["csv", "postgres"], default="csv")
    parser.add_argument("--init-db", action="store_true", help="Create schema and load CSVs into PostgreSQL")
    parser.add_argument("--season", type=int, help="Season to analyze (default: latest)")
    args = parser.parse_args()

    if args.init_db:
        init_db(get_engine())
        args.source = "postgres"

    df = analysis.load_data(args.source)
    season = args.season or int(df["season"].max())
    pd.set_option("display.width", 120)

    print(f"\n=== Top 10 Scorers ({season}) ===")
    print(analysis.top_players(df, season))
    print(f"\n=== Team Summary ({season}) ===")
    print(analysis.team_summary(df, season))
    print(f"\n=== Average Per-90 Stats by Position ({season}) ===")
    print(analysis.position_summary(df, season))

    star = analysis.top_players(df, season, n=1).loc[0, "player"]
    paths = [
        visualize.chart_top_scorers(df, season),
        visualize.chart_team_comparison(df, season),
        visualize.chart_team_trends(df),
        visualize.chart_shots_vs_goals(df, season),
        visualize.chart_player_trend(df, star),
    ]
    print("\nSaved charts:")
    for p in paths:
        print(" -", p)


if __name__ == "__main__":
    main()
