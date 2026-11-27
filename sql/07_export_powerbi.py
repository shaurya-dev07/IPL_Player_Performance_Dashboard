import csv
import os
import getpass
import oracledb

VIEWS = [
    "VW_PLAYER_BATTING",
    "VW_PLAYER_BOWLING",
    "VW_SEASON_BATTING",
    "VW_SEASON_BOWLING",
    "VW_PLAYER_COMPARISON",
    "VW_MATCH_RESULTS",
    "VW_TEAM_WINS",
    "VW_SEASON_RUNS",
    "VW_SEASON_MATCH_COUNTS",
    "VW_DIM_PLAYER",
    "VW_DIM_TEAM",
    "VW_DIM_SEASON",
    "VW_DIM_VENUE",
    "VW_DIM_DATE"
]

OUTPUT_DIR = "data/powerbi_export"
os.makedirs(OUTPUT_DIR, exist_ok=True)

password = getpass.getpass("Enter IPL_USER Oracle password: ")

connection = oracledb.connect(
    user="IPL_USER",
    password=password,
    dsn="localhost:1521/FREEPDB1"
)

try:
    cursor = connection.cursor()
    cursor.arraysize = 10000

    total_rows = 0

    for view in VIEWS:
        print(f"\nExporting {view}...")

        cursor.execute(f"SELECT * FROM {view}")

        columns = [column[0] for column in cursor.description]
        file_path = os.path.join(OUTPUT_DIR, f"{view}.csv")

        row_count = 0

        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(columns)

            while True:
                rows = cursor.fetchmany(10000)

                if not rows:
                    break

                writer.writerows(rows)
                row_count += len(rows)

        total_rows += row_count
        print(f"  Exported {row_count:,} rows -> {file_path}")

    print("\n===================================")
    print("EXPORT COMPLETED SUCCESSFULLY")
    print(f"Total views: {len(VIEWS)}")
    print(f"Total rows: {total_rows:,}")
    print(f"Output folder: {OUTPUT_DIR}")
    print("===================================")

finally:
    cursor.close()
    connection.close()
