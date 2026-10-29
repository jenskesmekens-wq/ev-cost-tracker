import sqlite3

from battery_daily_ratios import (
    get_daily_battery_ratios
)

conn = sqlite3.connect(
    "data/charging_history.db"
)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

ratios = get_daily_battery_ratios(
    "2026-10-22",
    "2026-10-28"
)

cur.execute("""
SELECT

    s.start_time,
    s.kwh,

    s.market_cost,
    s.actual_cost,
    s.savings,

    b.pv_direct_kwh,
    b.battery_kwh,
    b.grid_direct_kwh

FROM sessions s

LEFT JOIN session_energy_breakdown b
ON s.id = b.session_id

ORDER BY s.start_time DESC
""")

rows = cur.fetchall()

total_loaded = 0
total_market = 0
total_actual = 0
total_savings = 0

pv_direct_total = 0
battery_pv_total = 0
battery_grid_total = 0
grid_direct_total = 0

for row in rows:

    day = row["start_time"][:10]

    pv_ratio, grid_ratio = (
        ratios.get(
            day,
            (0, 1)
        )
    )

    battery = (
        row["battery_kwh"] or 0
    )

    pv_direct = (
        row["pv_direct_kwh"] or 0
    )

    grid_direct = (
        row["grid_direct_kwh"] or 0
    )

    battery_pv = (
        battery * pv_ratio
    )

    battery_grid = (
        battery * grid_ratio
    )

    total_loaded += (
        row["kwh"] or 0
    )

    total_market += (
        row["market_cost"] or 0
    )

    total_actual += (
        row["actual_cost"] or 0
    )

    total_savings += (
        row["savings"] or 0
    )

    pv_direct_total += pv_direct
    battery_pv_total += battery_pv
    battery_grid_total += battery_grid
    grid_direct_total += grid_direct

last = rows[0]

total_energy = (
    pv_direct_total +
    battery_pv_total +
    battery_grid_total +
    grid_direct_total
)

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>EV Cost Tracker</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background:#f4f6f8;
    margin:20px;
}}

h1 {{
    color:#1976d2;
}}

.cards {{
    display:flex;
    flex-wrap:wrap;
    gap:15px;
}}

.card {{
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 1px 4px rgba(0,0,0,.15);
    min-width:220px;
}}

.big {{
    font-size:26px;
    font-weight:bold;
}}

.green {{
    color:#2e7d32;
}}

.orange {{
    color:#ef6c00;
}}

.red {{
    color:#c62828;
}}

.blue {{
    color:#1565c0;
}}

table {{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}}

th {{
    background:#1976d2;
    color:white;
}}

th,td {{
    border:1px solid #ddd;
    padding:8px;
}}

</style>
</head>

<body>

<h1>EV Cost Tracker</h1>

<div class="cards">

<div class="card">
<div>Totaal geladen</div>
<div class="big">{total_loaded:.2f} kWh</div>
</div>

<div class="card">
<div>Marktkost</div>
<div class="big">€ {total_market:.2f}</div>
</div>

<div class="card">
<div>Werkelijke kost</div>
<div class="big">€ {total_actual:.2f}</div>
</div>

<div class="card">
<div>Besparing</div>
<div class="big green">
€ {total_savings:.2f}
</div>
</div>

<div class="card">
<div>Gem. werkelijke prijs</div>
<div class="big">
€ {(total_actual/total_loaded):.4f}/kWh
</div>
</div>

</div>

<h2>Laatste laadsessie</h2>

<div class="card">

<b>Datum:</b><br>
{last['start_time']}<br><br>

<b>kWh:</b>
{last['kwh']}<br>

<b>Marktkost:</b>
€ {last['market_cost']}<br>

<b>Werkelijke kost:</b>
€ {last['actual_cost']}<br>

<b>Besparing:</b>
€ {last['savings']}

</div>

<h2>Energieverdeling totaal</h2>

<div class="card">

PV direct:
<b>{pv_direct_total:.2f} kWh</b><br>

Battery PV:
<b>{battery_pv_total:.2f} kWh</b><br>

Battery GRID:
<b>{battery_grid_total:.2f} kWh</b><br>

Direct GRID:
<b>{grid_direct_total:.2f} kWh</b><br>

</div>

<h2>Historiek</h2>

<table>

<tr>
<th>Datum</th>
<th>kWh</th>
<th>Marktkost</th>
<th>Werkelijke kost</th>
<th>Besparing</th>
</tr>
"""

for row in rows:

    html += f"""
<tr>
<td>{row['start_time']}</td>
<td>{row['kwh']:.2f}</td>
<td>€ {row['market_cost'] or 0:.2f}</td>
<td>€ {row['actual_cost'] or 0:.2f}</td>
<td>€ {row['savings'] or 0:.2f}</td>
</tr>
"""

html += """
</table>

</body>
</html>
"""

with open(
    "docs/index.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(html)

print()
print("Dashboard gegenereerd:")
print("docs/index.html")
print()