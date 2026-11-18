async function load() {

    const res =
        await fetch(
            "dashboard.json"
        );

    const data =
        await res.json();

    initTabs();

    buildDashboard(
        data
    );

    buildHistory(
        data
    );

    buildMonthlyOverview(
        data
    );
}

function initTabs(){

    document
        .querySelectorAll(".tab")
        .forEach(btn => {

            btn.addEventListener(
                "click",
                () => {

                    document
                        .querySelectorAll(".tab")
                        .forEach(
                            t =>
                            t.classList.remove(
                                "active"
                            )
                        );

                    document
                        .querySelectorAll(".page")
                        .forEach(
                            p =>
                            p.classList.remove(
                                "active"
                            )
                        );

                    btn.classList.add(
                        "active"
                    );

                    document
                        .getElementById(
                            btn.dataset.page
                        )
                        .classList.add(
                            "active"
                        );
                }
            );
        });
}

function buildEnergyDonut(
    title,
    pv,
    batteryPv,
    batteryGrid,
    grid
){

    const total =
        pv +
        batteryPv +
        batteryGrid +
        grid;

    const pvPct =
        total ? (
            pv / total * 100
        ).toFixed(1) : 0;

    const batteryPvPct =
        total ? (
            batteryPv / total * 100
        ).toFixed(1) : 0;

    const batteryGridPct =
        total ? (
            batteryGrid / total * 100
        ).toFixed(1) : 0;

    const gridPct =
        total ? (
            grid / total * 100
        ).toFixed(1) : 0;

    return `

<div class="donut-card">

<h3>${title}</h3>

<svg
width="250"
height="250"
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
stroke-dasharray="${batteryPvPct} ${100-batteryPvPct}"
stroke-dashoffset="${25-pvPct}">
</circle>

<circle
cx="21"
cy="21"
r="15.915"
fill="transparent"
stroke="#FB8C00"
stroke-width="4"
stroke-dasharray="${batteryGridPct} ${100-batteryGridPct}"
stroke-dashoffset="${25-pvPct-batteryPvPct}">
</circle>

<circle
cx="21"
cy="21"
r="15.915"
fill="transparent"
stroke="#E53935"
stroke-width="4"
stroke-dasharray="${gridPct} ${100-gridPct}"
stroke-dashoffset="${25-pvPct-batteryPvPct-batteryGridPct}">
</circle>

</svg>

<div class="energy-line">
🟢 Direct PV:
${pv} kWh
(${pvPct}%)
</div>

<div class="energy-line">
🟩 Battery PV:
${batteryPv} kWh
(${batteryPvPct}%)
</div>

<div class="energy-line">
🟠 Battery GRID:
${batteryGrid} kWh
(${batteryGridPct}%)
</div>

<div class="energy-line">
🔴 Direct GRID:
${grid} kWh
(${gridPct}%)
</div>

</div>
`;
}

function buildDashboard(data){

    document.getElementById(
        "summary"
    ).innerHTML = `

<div class="card">
<div>Totaal geladen</div>
<div class="big">${data.summary.total_loaded}</div>
</div>

<div class="card">
<div>Marktkost</div>
<div class="big">€${data.summary.market_cost}</div>
</div>

<div class="card">
<div>Werkelijke kost</div>
<div class="big">€${data.summary.actual_cost}</div>
</div>

<div class="card">
<div>Besparing</div>
<div class="big green">€${data.summary.total_savings}</div>
</div>

<div class="card">
<div>Gem. werkelijke prijs</div>
<div class="big">€${data.summary.avg_actual_price}</div>
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

<b>Marktkost</b><br>
€${latest.market_cost}<br><br>

<b>Werkelijke kost</b><br>
€${latest.actual_cost}<br><br>

<b>Besparing</b><br>
€${latest.savings}

</div>
`;

    document.getElementById(
        "energy"
    ).innerHTML = `

<div class="donut-container">

${buildEnergyDonut(
    "Totale energieverdeling",
    data.energy_split.pv_direct,
    data.energy_split.battery_pv,
    data.energy_split.battery_grid,
    data.energy_split.grid_direct
)}

</div>
`;
}

function buildHistory(data){

    const tbody =
        document.querySelector(
            "#history tbody"
        );

    tbody.innerHTML = "";

    data.sessions.forEach(
        session => {

            tbody.innerHTML += `

<tr>
<td>${session.date}</td>
<td>${session.kwh}</td>
<td>€${session.market_cost}</td>
<td>€${session.actual_cost}</td>
<td>€${session.savings}</td>
<td>€${session.avg_cost_per_kwh}</td>
</tr>
`;
        }
    );
}

function buildMonthlyOverview(data){

    const selector =
        document.getElementById(
            "month-select"
        );

    const container =
        document.getElementById(
            "monthly-summary"
        );

    selector.innerHTML = "";

    const months =
        Object.keys(
            data.monthly_summary
        )
        .sort()
        .reverse();

    months.forEach(
        month => {

            selector.innerHTML += `
<option value="${month}">
${month}
</option>
`;
        }
    );

    function renderMonth(month){

        const m =
            data.monthly_summary[
                month
            ];

        container.innerHTML = `

<div class="cards">

<div class="card">
<div>Totaal geladen</div>
<div class="big">
${m.total_kwh}
</div>
</div>

<div class="card">
<div>Werkelijke kost</div>
<div class="big">
€${m.actual_cost}
</div>
</div>

<div class="card">
<div>Marktkost</div>
<div class="big">
€${m.market_cost}
</div>
</div>

<div class="card">
<div>Besparing</div>
<div class="big">
€${m.savings}
</div>
</div>

<div class="card">
<div>Gem. kost per kWh</div>
<div class="big">
€${m.avg_cost_per_kwh}
</div>
</div>

</div>

<div class="donut-container">

${buildEnergyDonut(
    month,
    m.pv_direct,
    m.battery_pv,
    m.battery_grid,
    m.grid_direct
)}

</div>
`;
    }

    selector.addEventListener(
        "change",
        () => {

            renderMonth(
                selector.value
            );
        }
    );

    if(months.length > 0){

        renderMonth(
            months[0]
        );
    }
}

load();