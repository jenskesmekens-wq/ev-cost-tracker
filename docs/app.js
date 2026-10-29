async function load(){

    const res =
        await fetch(
            "dashboard.json"
        );

    const data =
        await res.json();

    document.getElementById(
        "summary"
    ).innerHTML = `

    <div class="card">
        <div>Totaal geladen</div>
        <div class="big">
            ${data.summary.total_loaded}
        </div>
    </div>

    <div class="card">
        <div>Marktkost</div>
        <div class="big">
            €${data.summary.market_cost}
        </div>
    </div>

    <div class="card">
        <div>Werkelijke kost</div>
        <div class="big">
            €${data.summary.actual_cost}
        </div>
    </div>

    <div class="card">
        <div>Besparing</div>
        <div class="big green">
            €${data.summary.total_savings}
        </div>
    </div>

    <div class="card">
        <div>Gem. werkelijke prijs</div>
        <div class="big">
            €${data.summary.avg_actual_price}
        </div>
    </div>

    <div class="card">
        <div>Dekkingsgraad</div>
        <div class="big coverage">
            94.9%
        </div>
    </div>
    `;

    const latest =
        data.latest_session;

    document.getElementById(
        "latest"
    ).innerHTML = `

    <div class="card">

        <h3>Laatste sessie</h3>

        <b>Datum</b><br>
        ${latest.date}<br><br>

        <b>kWh geladen</b><br>
        ${latest.kwh}<br><br>

        <b>Direct PV</b><br>
        ${latest.pv_direct} kWh<br><br>

        <b>Battery PV</b><br>
        ${latest.battery_pv} kWh<br><br>

        <b>Battery GRID</b><br>
        ${latest.battery_grid} kWh<br><br>

        <b>Direct GRID</b><br>
        ${latest.grid_direct} kWh<br><br>

        <b>Marktkost</b><br>
        €${latest.market_cost}<br><br>

        <b>Werkelijke kost</b><br>
        €${latest.actual_cost}<br><br>

        <b>Besparing</b><br>
        €${latest.savings}

    </div>
    `;

    const e =
        data.energy_split;

    const total =
        e.pv_direct +
        e.battery_pv +
        e.battery_grid +
        e.grid_direct;

    const pvPct =
        ((e.pv_direct / total) * 100).toFixed(1);

    const batPvPct =
        ((e.battery_pv / total) * 100).toFixed(1);

    const batGridPct =
        ((e.battery_grid / total) * 100).toFixed(1);

    const gridPct =
        ((e.grid_direct / total) * 100).toFixed(1);

    document.getElementById(
        "energy"
    ).innerHTML = `

    <div class="card energy-card">

    <svg width="300"
         height="300"
         viewBox="0 0 42 42">

        <circle
            cx="21"
            cy="21"
            r="15.915"
            fill="transparent"
            stroke="#ddd"
            stroke-width="4">
        </circle>

        <circle
            cx="21"
            cy="21"
            r="15.915"
            fill="transparent"
            stroke="#2E7D32"
            stroke-width="4"
            stroke-dasharray="${pvPct} ${100-pvPct}"
            stroke-dashoffset="25">
        </circle>

        <circle
            cx="21"
            cy="21"
            r="15.915"
            fill="transparent"
            stroke="#66BB6A"
            stroke-width="4"
            stroke-dasharray="${batPvPct} ${100-batPvPct}"
            stroke-dashoffset="${25-pvPct}">
        </circle>

        <circle
            cx="21"
            cy="21"
            r="15.915"
            fill="transparent"
            stroke="#FB8C00"
            stroke-width="4"
            stroke-dasharray="${batGridPct} ${100-batGridPct}"
            stroke-dashoffset="${25-pvPct-batPvPct}">
        </circle>

        <circle
            cx="21"
            cy="21"
            r="15.915"
            fill="transparent"
            stroke="#E53935"
            stroke-width="4"
            stroke-dasharray="${gridPct} ${100-gridPct}"
            stroke-dashoffset="${25-pvPct-batPvPct-batGridPct}">
        </circle>

    </svg>

    <br><br>

    🟢 Direct PV:
    ${e.pv_direct} kWh (${pvPct}%)

    <br><br>

    🟩 Battery PV:
    ${e.battery_pv} kWh (${batPvPct}%)

    <br><br>

    🟠 Battery GRID:
    ${e.battery_grid} kWh (${batGridPct}%)

    <br><br>

    🔴 Direct GRID:
    ${e.grid_direct} kWh (${gridPct}%)

    </div>
    `;

    const tbody =
        document.querySelector(
            "#history tbody"
        );

    tbody.innerHTML = "";

    data.sessions.forEach(
        s => {

            tbody.innerHTML += `
            <tr>
                <td>${s.date}</td>
                <td>${s.kwh}</td>
                <td>€${s.market_cost}</td>
                <td>€${s.actual_cost}</td>
                <td>€${s.savings}</td>
            </tr>
            `;
        }
    );
}

load();