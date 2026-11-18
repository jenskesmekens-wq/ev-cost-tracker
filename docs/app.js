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


function initTabs() {

    document
        .querySelectorAll(".tab")
        .forEach(button => {

            button.addEventListener(
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

                    button.classList.add(
                        "active"
                    );

                    document
                        .getElementById(
                            button.dataset.page
                        )
                        .classList.add(
                            "active"
                        );
                }
            );
        });
}


function buildDashboard(
    data
) {

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

    document.getElementById(
        "energy"
    ).innerHTML = `

<div class="card">

<h3>Energieverdeling</h3>

<p>
🟢 Direct PV:
${e.pv_direct} kWh
</p>

<p>
🟩 Battery PV:
${e.battery_pv} kWh
</p>

<p>
🟠 Battery GRID:
${e.battery_grid} kWh
</p>

<p>
🔴 Direct GRID:
${e.grid_direct} kWh
</p>

</div>
`;
}


function buildHistory(
    data
) {

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

<td>
€${session.market_cost}
</td>

<td>
€${session.actual_cost}
</td>

<td>
€${session.savings}
</td>

<td>
€${session.avg_cost_per_kwh}
</td>

</tr>
`;
        }
    );
}


function buildMonthlyOverview(
    data
) {

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

    function renderMonth(
        month
    ) {

        const m =
            data.monthly_summary[
                month
            ];

        container.innerHTML = `

<div class="card">

<h3>
${month}
</h3>

<p>
⚡ Totaal geladen:
${m.total_kwh} kWh
</p>

<p>
💰 Werkelijke kost:
€${m.actual_cost}
</p>

<p>
📈 Marktkost:
€${m.market_cost}
</p>

<p>
🎯 Besparing:
€${m.savings}
</p>

<p>
📊 Gem. kost per kWh:
€${m.avg_cost_per_kwh}
</p>

</div>

<div class="card">

<h3>
Energieverdeling
</h3>

<p>
🟢 Direct PV:
${m.pv_direct} kWh
</p>

<p>
🟩 Battery PV:
${m.battery_pv} kWh
</p>

<p>
🟠 Battery GRID:
${m.battery_grid} kWh
</p>

<p>
🔴 Direct GRID:
${m.grid_direct} kWh
</p>

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

    if (
        months.length > 0
    ) {

        renderMonth(
            months[0]
        );
    }
}


load();