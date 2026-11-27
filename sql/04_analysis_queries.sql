-- =====================================================
-- IPL PLAYER PERFORMANCE DASHBOARD
-- ADVANCED ANALYSIS QUERIES
-- Oracle Database 26ai
-- =====================================================

SET PAGESIZE 100
SET LINESIZE 180
SET FEEDBACK ON

PROMPT ==========================================
PROMPT 1. TOP 10 BATTERS USING DENSE_RANK
PROMPT ==========================================

SELECT BATTER, RUNS, BATTING_AVERAGE, STRIKE_RATE, PLAYER_RANK
FROM (
    SELECT BATTER,
           RUNS,
           BATTING_AVERAGE,
           STRIKE_RATE,
           DENSE_RANK() OVER (ORDER BY RUNS DESC) AS PLAYER_RANK
    FROM BATTING_STATS
)
WHERE PLAYER_RANK <= 10
ORDER BY PLAYER_RANK, BATTER;

PROMPT ==========================================
PROMPT 2. TOP 10 BOWLERS USING DENSE_RANK
PROMPT ==========================================

SELECT BOWLER, WICKETS, ECONOMY, BOWLING_AVERAGE, PLAYER_RANK
FROM (
    SELECT BOWLER,
           WICKETS,
           ECONOMY,
           BOWLING_AVERAGE,
           DENSE_RANK() OVER (ORDER BY WICKETS DESC) AS PLAYER_RANK
    FROM BOWLING_STATS
)
WHERE PLAYER_RANK <= 10
ORDER BY PLAYER_RANK, BOWLER;

PROMPT ==========================================
PROMPT 3. SEASON-WISE TOP 3 BATTERS
PROMPT ==========================================

SELECT SEASON, BATTER, RUNS, STRIKE_RATE, SEASON_RANK
FROM (
    SELECT SEASON,
           BATTER,
           RUNS,
           STRIKE_RATE,
           DENSE_RANK() OVER (
               PARTITION BY SEASON
               ORDER BY RUNS DESC
           ) AS SEASON_RANK
    FROM SEASON_BATTING_STATS
)
WHERE SEASON_RANK <= 3
ORDER BY SEASON, SEASON_RANK, BATTER;

PROMPT ==========================================
PROMPT 4. SEASON-WISE TOP 3 BOWLERS
PROMPT ==========================================

SELECT SEASON, BOWLER, WICKETS, ECONOMY, SEASON_RANK
FROM (
    SELECT SEASON,
           BOWLER,
           WICKETS,
           ECONOMY,
           DENSE_RANK() OVER (
               PARTITION BY SEASON
               ORDER BY WICKETS DESC
           ) AS SEASON_RANK
    FROM SEASON_BOWLING_STATS
)
WHERE SEASON_RANK <= 3
ORDER BY SEASON, SEASON_RANK, BOWLER;

PROMPT ==========================================
PROMPT 5. PLAYER COMPARISON
PROMPT ==========================================

WITH SELECTED_PLAYERS AS (
    SELECT 'V Kohli' AS PLAYER FROM DUAL
    UNION ALL
    SELECT 'DA Warner' FROM DUAL
)
SELECT P.PLAYER,
       B.INNINGS AS BATTING_INNINGS,
       B.RUNS,
       B.BATTING_AVERAGE,
       B.STRIKE_RATE,
       BW.WICKETS,
       BW.ECONOMY,
       BW.BOWLING_AVERAGE
FROM SELECTED_PLAYERS P
LEFT JOIN BATTING_STATS B
    ON P.PLAYER = B.BATTER
LEFT JOIN BOWLING_STATS BW
    ON P.PLAYER = BW.BOWLER
ORDER BY P.PLAYER;

PROMPT ==========================================
PROMPT 6. TEAM-WISE MATCH WINS
PROMPT ==========================================

SELECT WINNER AS TEAM,
       COUNT(*) AS TOTAL_WINS
FROM MATCHES
WHERE WINNER IS NOT NULL
GROUP BY WINNER
ORDER BY TOTAL_WINS DESC;

PROMPT ==========================================
PROMPT 7. SEASON-WISE TOTAL RUNS
PROMPT ==========================================

SELECT SEASON,
       SUM(RUNS) AS TOTAL_RUNS,
       COUNT(DISTINCT BATTER) AS ACTIVE_BATTERS
FROM SEASON_BATTING_STATS
GROUP BY SEASON
ORDER BY SEASON;

PROMPT ==========================================
PROMPT ADVANCED ANALYSIS COMPLETED
PROMPT ==========================================
