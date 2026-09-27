"""One-off: record status + first bytes of each data endpoint so the builder can be written against real shapes."""
import json, pathlib, urllib.request, urllib.parse

UA = {"User-Agent": "Mozilla/5.0 (nhl-data personal research script)"}
S = "https://api.nhle.com/stats/rest/en"
W = "https://api-web.nhle.com/v1"
MP = "https://moneypuck.com/moneypuck/playerData/seasonSummary"
sort = urllib.parse.quote('[{"property":"gameDate","direction":"ASC"},{"property":"playerId","direction":"ASC"}]')
def cay(e): return urllib.parse.quote(e)
g = 'seasonId=20252026 and gameTypeId=2 and gameDate<="2025-10-10 23:59:59"'
urls = {
 "skater_summary_game": f"{S}/skater/summary?isAggregate=false&isGame=true&start=0&limit=3&sort={sort}&cayenneExp={cay(g)}",
 "skater_toi_game": f"{S}/skater/timeonice?isAggregate=false&isGame=true&start=0&limit=3&sort={sort}&cayenneExp={cay(g)}",
 "goalie_summary_game": f"{S}/goalie/summary?isAggregate=false&isGame=true&start=0&limit=3&sort={sort}&cayenneExp={cay(g)}",
 "skater_summary_game_limit_all": f"{S}/skater/summary?isAggregate=false&isGame=true&start=0&limit=-1&sort={sort}&cayenneExp={cay(g)}",
 "skater_toi_agg": f"{S}/skater/timeonice?isAggregate=true&isGame=false&start=0&limit=3&cayenneExp={cay('seasonId=20252026 and gameTypeId=2')}",
 "skater_summary_agg": f"{S}/skater/summary?isAggregate=true&isGame=false&start=0&limit=3&cayenneExp={cay('seasonId=20252026 and gameTypeId=2')}",
 "team_summary": f"{S}/team/summary?isAggregate=false&isGame=false&start=0&limit=3&cayenneExp={cay('seasonId=20252026 and gameTypeId=2')}",
 "team_list": f"{S}/team",
 "schedule_today": f"{W}/schedule/2026-09-27",
 "schedule_oct": f"{W}/schedule/2026-10-12",
 "roster_edm": f"{W}/roster/EDM/current",
 "standings": f"{W}/standings/now",
 "mp_teams_2025": f"{MP}/2025/regular/teams.csv",
 "mp_goalies_2025": f"{MP}/2025/regular/goalies.csv",
 "mp_skaters_2025": f"{MP}/2025/regular/skaters.csv",
 "mp_teams_2026": f"{MP}/2026/regular/teams.csv",
}
out = pathlib.Path("probe"); out.mkdir(exist_ok=True)
summary = {}
for k, u in urls.items():
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
            b = r.read(); summary[k] = {"status": r.status, "bytes": len(b)}
            txt = b.decode("utf-8", "replace")
            if k.endswith("limit_all"):
                d = json.loads(txt); summary[k]["rows"] = len(d.get("data", [])); summary[k]["total"] = d.get("total")
                txt = txt[:1500]
            (out / f"{k}.txt").write_text(txt[:6000])
    except Exception as e:
        summary[k] = {"error": repr(e)[:300]}
(out / "_summary.json").write_text(json.dumps(summary, indent=1))
print(json.dumps(summary, indent=1))
