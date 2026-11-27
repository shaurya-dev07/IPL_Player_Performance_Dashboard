# IPL Player Performance Dashboard

A data analytics project focused on exploring and analyzing Indian Premier League (IPL) cricket statistics using Python, Oracle SQL, and Power BI.

The project involves processing IPL match and ball-by-ball data, storing structured information in an Oracle database, creating analytical SQL views, and developing an interactive Power BI dashboard to understand player, team, and season-wise performance.

## Project Description

The objective of this project is to analyze historical IPL data and present meaningful insights through data visualization.

The project covers the complete data analytics workflow, from data preparation and database management to dashboard development.

## Technologies Used

- **Python:** Data cleaning, preprocessing, and data export.
- **Pandas:** Data manipulation and analysis.
- **Oracle Database 26ai Free:** Data storage and database management.
- **SQL:** Table creation, data validation, analytical queries, and views.
- **Power BI Desktop:** Interactive dashboard development.
- **DAX:** Measures and player comparison calculations.
- **Jupyter Notebook:** Exploratory data analysis.

## Dataset

The project uses IPL historical match and ball-by-ball delivery data.

**Dataset source:** [IPL Complete Dataset (2008–2024) – Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)

The main datasets used are:

| File | Description |
|---|---|
| `matches.csv` | IPL match information |
| `deliveries.csv` | Ball-by-ball delivery information |

### Processed Data

The following datasets were prepared for analysis:

- Batting statistics
- Bowling statistics
- Season-wise batting statistics
- Season-wise bowling statistics
- Cleaned match data
- Cleaned delivery data

### Dataset Statistics

| Dataset | Records |
|---|---:|
| Matches | 1,095 |
| Deliveries | 260,920 |
| Batting Statistics | 673 |
| Bowling Statistics | 530 |
| Season Batting Statistics | 2,617 |
| Season Bowling Statistics | 1,948 |

The available 2024 dataset contains 71 matches, so the analysis for that season is based on the available records.

## Database Design

Oracle Database is used to store the processed IPL data and perform SQL-based analysis.

### Tables Created

1. `MATCHES`
2. `DELIVERIES`
3. `BATTING_STATS`
4. `BOWLING_STATS`
5. `SEASON_BATTING_STATS`
6. `SEASON_BOWLING_STATS`

### SQL Views Created

A total of 14 views were created to organize data for analysis and Power BI reporting.

**Player Analysis**
- `VW_PLAYER_BATTING`
- `VW_PLAYER_BOWLING`
- `VW_PLAYER_COMPARISON`

**Season Analysis**
- `VW_SEASON_BATTING`
- `VW_SEASON_BOWLING`
- `VW_SEASON_RUNS`
- `VW_SEASON_MATCH_COUNTS`

**Team and Match Analysis**
- `VW_MATCH_RESULTS`
- `VW_TEAM_WINS`

**Dimension Views**
- `VW_DIM_PLAYER`
- `VW_DIM_TEAM`
- `VW_DIM_SEASON`
- `VW_DIM_VENUE`
- `VW_DIM_DATE`

## Power BI Dashboard

The Power BI report currently contains four pages.

### 1. IPL Overview

Provides an overall summary of IPL statistics.

- Total IPL matches
- Total runs scored
- Total wickets
- Total teams
- Season-wise runs
- Season-wise matches
- Team-wise wins
- Top 10 run scorers
- Top 10 wicket takers

### 2. Batting Analysis

Focuses on player batting performance.

- Total batter runs
- Total IPL batters
- Total balls faced
- Average batting average
- Total dismissals
- Average strike rate
- Top 10 run scorers
- Top batters by average
- Top batters by strike rate
- Season-wise batting runs
- Detailed batting statistics

### 3. Bowling Analysis

Focuses on player bowling performance.

- Total wickets
- Total IPL bowlers
- Total balls bowled
- Average economy
- Average bowling average
- Average bowling strike rate
- Top 10 wicket takers
- Economical bowlers with a minimum balls-bowled filter
- Season-wise wickets
- Detailed bowling statistics

### 4. Player Comparison

Allows comparison between two selected players.

- Separate Player 1 and Player 2 selection
- Total runs comparison
- Batting innings
- Batting average
- Total wickets comparison
- Bowling innings
- Economy rate
- Visual comparison of runs and wickets

## Key Statistics

Some of the figures currently available in the dashboard include:

| Metric | Value |
|---|---:|
| Total IPL Matches | 1,095 |
| Total Runs (including extras) | 347,756 |
| Total Batter Runs | 330,064 |
| Total Wickets | 11,815 |
| Total Teams | 15 |
| Unique Players | 732 |
| Unique Venues | 58 |

## Project Workflow

The project follows these main steps:

1. Collect IPL match and delivery datasets.
2. Clean and preprocess data using Python.
3. Perform exploratory data analysis.
4. Create relational tables in Oracle Database.
5. Load processed data into Oracle.
6. Perform data validation using SQL.
7. Create analytical and dimension views.
8. Export SQL views into CSV files.
9. Import the exported data into Power BI.
10. Create relationships, measures, charts, and interactive dashboard pages.

## Project Structure

```text
IPL_Player_Performance_Dashboard/
│
├── data/
│   ├── cleaned/
│   ├── processed/
│   └── powerbi_export/
│
├── python/
│   └── IPL_Analysis.ipynb
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_load_data.py
│   ├── 03_validation.sql
│   ├── 04_analysis_queries.sql
│   ├── 05_create_views.sql
│   ├── 06_create_dimensions.sql
│   └── 07_export_powerbi.py
│
├── IPL_Player_Performance_Dashboard.pbix
└── README.md
```

## Current Project Status

The project currently includes:

- Data cleaning and preprocessing
- Oracle database table creation and data loading
- SQL data validation
- 14 analytical and dimension views
- Export of SQL views for Power BI
- Power BI data modeling and relationships
- Four dashboard pages with interactive slicers and visualizations
- PDF export of the dashboard

Further improvements and enhancements may be added as the project develops.

## Future Improvements

- Include additional IPL seasons and updated datasets.
- Improve dashboard design and visual formatting.
- Add more advanced player performance metrics.
- Explore player performance trends and predictive analytics.
- Improve automation of data processing and refresh workflows.

## Author

**Shaurya Pratap Singh**

**Project:** IPL Player Performance Dashboard

**Technologies:** Python | Oracle SQL | Power BI | DAX
