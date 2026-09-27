# nhl-data

Daily NHL data for a personal Bet365 moneyline model.

A GitHub Action (`.github/workflows/build.yml`) runs every morning at 13:30 UTC (6:30am PDT) and:

1. Pulls per-game skater and goalie logs, schedules, rosters and team stats from the NHL's public APIs, and team/goalie season summaries from MoneyPuck.
2. Builds `output/nhl_daily_data.xlsx` (README, Schedule, Goalies, Teams, Skaters tabs), matching CSVs, `meta.json`, and `index.html`.
3. Commits the results. Game logs accumulate in `data/<season>/`.

Run it manually from the Actions tab ("daily-build" → Run workflow). Filling in `build_date` runs a test as if it were that date and writes to `test/` instead.

Rules for goalie tiers, skater roles and hot/cold labels are at the top of `scripts/build.py`.
