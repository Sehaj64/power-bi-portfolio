-- ==============================================================================
-- 📂 CASE STUDY 4: IPL CRICKET PLAYER & TEAM PERFORMANCE METRICS
-- ==============================================================================

-- 🔍 PROBLEM STATEMENT:
-- Franchise coaches and analysts want to select players for the next auction.
-- We must calculate batsman strike rates in the death overs, identify the most 
-- economical bowlers in powerplays, and evaluate team chasing success rates.
-- (This case study references an IPL schema: matches, deliveries, and players).

-- ------------------------------------------------------------------------------
-- Task 1: Find Top 5 Batsmen by Strike Rate in "Death Overs" (Overs 16 to 20).
-- (Criteria: Minimum of 100 balls faced in death overs).
-- ------------------------------------------------------------------------------
SELECT 
    batsman,
    SUM(batsman_runs) AS total_runs,
    COUNT(ball) AS total_balls_faced,
    ROUND((SUM(batsman_runs)::numeric / COUNT(ball) * 100), 2) AS death_over_strike_rate
FROM deliveries
WHERE over >= 16
GROUP BY batsman
HAVING COUNT(ball) >= 100
ORDER BY death_over_strike_rate DESC
LIMIT 5;

-- 💡 Insight: Pinpoints the most effective "finishers" in cricket. High strike rates in the 
-- final 5 overs can dramatically shift game outcomes and represent key auction targets.


-- ------------------------------------------------------------------------------
-- Task 2: Identify the most economical Bowlers in "Powerplay" (Overs 1 to 6).
-- (Criteria: Minimum of 20 overs bowled in powerplays).
-- ------------------------------------------------------------------------------
WITH powerplay_bowlers AS (
    SELECT 
        bowler,
        SUM(total_runs) - SUM(bye_runs) - SUM(legbye_runs) AS bowler_conceded_runs,
        COUNT(CASE WHEN wide_runs = 0 AND noball_runs = 0 THEN 1 END) AS valid_balls
    FROM deliveries
    WHERE over <= 6
    GROUP BY bowler
    HAVING COUNT(CASE WHEN wide_runs = 0 AND noball_runs = 0 THEN 1 END) >= 120 -- 20 overs = 120 balls
)
SELECT 
    bowler,
    ROUND((bowler_conceded_runs::numeric / (valid_balls / 6.0)), 2) AS economy_rate,
    ROUND(valid_balls / 6.0, 1) AS overs_bowled
FROM powerplay_bowlers
ORDER BY economy_rate ASC
LIMIT 5;

-- 💡 Insight: Identifies defensive bowling assets who can prevent early runs, putting pressure 
-- on the opposition's opening batsmen.


-- ------------------------------------------------------------------------------
-- Task 3: Calculate the Team Chasing Success Rate when batting second.
-- ------------------------------------------------------------------------------
WITH chasing_records AS (
    SELECT 
        winner AS team,
        COUNT(match_id) AS matches_won_chasing
    FROM matches
    WHERE toss_decision = 'field' AND toss_winner = winner
       OR toss_decision = 'bat' AND toss_winner != winner
    GROUP BY winner
),
total_chases AS (
    SELECT 
        team2 AS team,
        COUNT(match_id) AS total_chasing_matches
    FROM matches
    GROUP BY team2
)
SELECT 
    tc.team,
    tc.total_chasing_matches,
    COALESCE(cr.matches_won_chasing, 0) AS chases_won,
    ROUND((COALESCE(cr.matches_won_chasing, 0)::numeric / tc.total_chasing_matches * 100), 2) AS chase_win_rate_percent
FROM total_chases tc
LEFT JOIN chasing_records cr ON tc.team = cr.team
WHERE tc.total_chasing_matches >= 10
ORDER BY chase_win_rate_percent DESC;

-- 💡 Insight: Guides tactical decisions. If a team has a >65% chase win rate, they should 
-- prioritize fielding first upon winning the coin toss.
