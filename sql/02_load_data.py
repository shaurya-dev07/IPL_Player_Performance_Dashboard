
import csv
import os
import getpass
from datetime import datetime

import oracledb

# =====================================================
# IPL PLAYER PERFORMANCE DASHBOARD
# CSV TO ORACLE BULK IMPORTER
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

BATCH_SIZE = 5000

# Numeric columns that should be converted to integers
INTEGER_COLUMNS = {
    "ID", "INNING", "OVER_NUMBER", "BALL_NUMBER",
    "BATSMAN_RUNS", "EXTRA_RUNS", "TOTAL_RUNS",
    "IS_WICKET", "BOWLER_RUNS", "LEGAL_BALL",
    "INNINGS", "RUNS", "BALLS_FACED", "DISMISSALS",
    "RUNS_CONCEDED", "BALLS_BOWLED", "WICKETS"
}

# Numeric columns that may contain decimal values
FLOAT_COLUMNS = {
    "RESULT_MARGIN", "TARGET_RUNS", "TARGET_OVERS",
    "BATTING_AVERAGE", "STRIKE_RATE", "OVERS",
    "ECONOMY", "BOWLING_AVERAGE",
    "BOWLING_STRIKE_RATE", "AVERAGE"
}

# Source CSV headers mapped to Oracle table columns
DATASETS = [
    {
        "file": "cleaned/matches_clean.csv",
        "table": "MATCHES",
        "columns": [
            ("id", "ID"),
            ("season", "SEASON"),
            ("city", "CITY"),
            ("date", "MATCH_DATE"),
            ("match_type", "MATCH_TYPE"),
            ("player_of_match", "PLAYER_OF_MATCH"),
            ("venue", "VENUE"),
            ("team1", "TEAM1"),
            ("team2", "TEAM2"),
            ("toss_winner", "TOSS_WINNER"),
            ("toss_decision", "TOSS_DECISION"),
            ("winner", "WINNER"),
            ("result", "RESULT"),
            ("result_margin", "RESULT_MARGIN"),
            ("target_runs", "TARGET_RUNS"),
            ("target_overs", "TARGET_OVERS"),
            ("super_over", "SUPER_OVER"),
            ("method", "METHOD"),
            ("umpire1", "UMPIRE1"),
            ("umpire2", "UMPIRE2")
        ]
    },
    {
        "file": "cleaned/deliveries_clean.csv",
        "table": "DELIVERIES",
        "columns": [
            ("match_id", "MATCH_ID"),
            ("inning", "INNING"),
            ("batting_team", "BATTING_TEAM"),
            ("bowling_team", "BOWLING_TEAM"),
            ("over", "OVER_NUMBER"),
            ("ball", "BALL_NUMBER"),
            ("batter", "BATTER"),
            ("bowler", "BOWLER"),
            ("non_striker", "NON_STRIKER"),
            ("batsman_runs", "BATSMAN_RUNS"),
            ("extra_runs", "EXTRA_RUNS"),
            ("total_runs", "TOTAL_RUNS"),
            ("extras_type", "EXTRAS_TYPE"),
            ("is_wicket", "IS_WICKET"),
            ("player_dismissed", "PLAYER_DISMISSED"),
            ("dismissal_kind", "DISMISSAL_KIND"),
            ("fielder", "FIELDER"),
            ("innings_id", "INNINGS_ID"),
            ("bowler_runs", "BOWLER_RUNS"),
            ("legal_ball", "LEGAL_BALL")
        ]
    },
    {
        "file": "processed/batting_stats.csv",
        "table": "BATTING_STATS",
        "columns": [
            ("batter", "BATTER"),
            ("innings", "INNINGS"),
            ("runs", "RUNS"),
            ("balls_faced", "BALLS_FACED"),
            ("dismissals", "DISMISSALS"),
            ("batting_average", "BATTING_AVERAGE"),
            ("strike_rate", "STRIKE_RATE")
        ]
    },
    {
        "file": "processed/bowling_stats.csv",
        "table": "BOWLING_STATS",
        "columns": [
            ("bowler", "BOWLER"),
            ("innings", "INNINGS"),
            ("runs_conceded", "RUNS_CONCEDED"),
            ("balls_bowled", "BALLS_BOWLED"),
            ("wickets", "WICKETS"),
            ("overs", "OVERS"),
            ("economy", "ECONOMY"),
            ("bowling_average", "BOWLING_AVERAGE"),
            ("bowling_strike_rate", "BOWLING_STRIKE_RATE")
        ]
    },
    {
        "file": "processed/season_batting_stats.csv",
        "table": "SEASON_BATTING_STATS",
        "columns": [
            ("season", "SEASON"),
            ("batter", "BATTER"),
            ("runs", "RUNS"),
            ("balls_faced", "BALLS_FACED"),
            ("innings", "INNINGS"),
            ("dismissals", "DISMISSALS"),
            ("average", "AVERAGE"),
            ("strike_rate", "STRIKE_RATE")
        ]
    },
    {
        "file": "processed/season_bowling_stats.csv",
        "table": "SEASON_BOWLING_STATS",
        "columns": [
            ("season", "SEASON"),
            ("bowler", "BOWLER"),
            ("innings", "INNINGS"),
            ("runs_conceded", "RUNS_CONCEDED"),
            ("balls_bowled", "BALLS_BOWLED"),
            ("wickets", "WICKETS"),
            ("overs", "OVERS"),
            ("economy", "ECONOMY"),
            ("bowling_average", "BOWLING_AVERAGE"),
            ("bowling_strike_rate", "BOWLING_STRIKE_RATE")
        ]
    }
]


def convert_value(value, target_column):

    if value is None:
        return None

    value = value.strip()

    if value.lower() in ("", "nan", "none", "null"):
        return None

    if target_column == "MATCH_DATE":
        return datetime.strptime(value, "%Y-%m-%d")

    if target_column == "LEGAL_BALL":
        return 1 if value.lower() == "true" else 0

    if target_column in INTEGER_COLUMNS:
        return int(value)

    if target_column in FLOAT_COLUMNS:
        return float(value)

    return value


def load_dataset(cursor, connection, dataset):

    table = dataset["table"]
    file_path = os.path.join(DATA_DIR, dataset["file"])
    columns = dataset["columns"]

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    # Prevent accidental duplicate imports
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        raise RuntimeError(
            f"{table} already contains {existing_count} rows. "
            "Import cancelled to prevent duplicates."
        )

    target_columns = [target for source, target in columns]

    placeholders = ", ".join(
        f":{i + 1}" for i in range(len(target_columns))
    )

    column_names = ", ".join(target_columns)

    sql = (
        f"INSERT INTO {table} ({column_names}) "
        f"VALUES ({placeholders})"
    )

    batch = []
    total_rows = 0

    print(f"\nLoading {table}...")

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        expected_headers = [source for source, target in columns]

        if reader.fieldnames != expected_headers:
            raise ValueError(
                f"Unexpected CSV headers in {file_path}\n"
                f"Expected: {expected_headers}\n"
                f"Found: {reader.fieldnames}"
            )

        for row in reader:

            converted_row = tuple(
                convert_value(row[source], target)
                for source, target in columns
            )

            batch.append(converted_row)

            if len(batch) >= BATCH_SIZE:
                cursor.executemany(sql, batch)
                total_rows += len(batch)
                batch.clear()

        if batch:
            cursor.executemany(sql, batch)
            total_rows += len(batch)

    connection.commit()

    print(f"Successfully loaded {total_rows:,} rows into {table}")

    return total_rows


def main():

    username = "IPL_USER"
    password = getpass.getpass("Enter IPL_USER database password: ")

    connection = None

    try:

        connection = oracledb.connect(
            user=username,
            password=password,
            dsn="localhost:1521/FREEPDB1"
        )

        cursor = connection.cursor()

        print("\nConnected to Oracle Database 26ai!")
        print("Starting IPL CSV import...")

        results = {}

        for dataset in DATASETS:

            count = load_dataset(
                cursor,
                connection,
                dataset
            )

            results[dataset["table"]] = count

        print("\n========== IMPORT SUMMARY ==========")

        for table, count in results.items():
            print(f"{table:<25} {count:>10,}")

        print("\nAll six datasets imported successfully!")

    except Exception as error:

        if connection:
            connection.rollback()

        print("\nIMPORT FAILED:")
        print(error)

        raise

    finally:

        if connection:
            connection.close()
            print("\nOracle connection closed.")


if __name__ == "__main__":
    main()
