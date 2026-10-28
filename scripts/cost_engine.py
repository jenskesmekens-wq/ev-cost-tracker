from datetime import datetime, timedelta


def engie_total_price(market_price):
    """
    market_price komt uit prices.json in €/kWh.

    We zetten eerst om naar €/MWh omdat
    de formule in Energieprijs-Zele met €/MWh werkt.

    Resultaat:
    volledige afnameprijs in €/kWh.
    """

    spot_mwh = market_price * 1000

    b = 6.714
    m = 0.1039

    vat = 1.06

    net = 5.27945
    exc = 4.876

    energy_cents = (
        b +
        (m * spot_mwh)
    ) * vat

    total_cents = (
        energy_cents +
        net +
        exc
    )

    return total_cents / 100


def get_quarter_prices(price_data):

    prices = {}

    today = (
        price_data
        .get("today", {})
        .get("data", [])
    )

    for item in today:

        ts = datetime.fromisoformat(
            item["timestamp"]
            .replace("Z", "+00:00")
        ).replace(
            tzinfo=None
        )

        prices[ts] = float(
            item["price_eur_kwh"]
        )

    tomorrow = price_data.get(
        "tomorrow",
        {}
    )

    if isinstance(
        tomorrow,
        dict
    ):

        for item in tomorrow.get(
            "data",
            []
        ):

            ts = datetime.fromisoformat(
                item["timestamp"]
                .replace("Z", "+00:00")
            ).replace(
                tzinfo=None
            )

            prices[ts] = float(
                item["price_eur_kwh"]
            )

    return prices


def calculate_session_market_price(
        start_time,
        end_time,
        total_kwh,
        price_lookup
):

    duration_hours = (
        end_time -
        start_time
    ).total_seconds() / 3600

    if duration_hours <= 0:
        return (
            0.0,
            0.0
        )

    avg_power = (
        total_kwh /
        duration_hours
    )

    current = start_time

    total_cost = 0.0
    total_energy = 0.0

    while current < end_time:

        quarter_end = min(
            current +
            timedelta(minutes=15),
            end_time
        )

        hours = (
            quarter_end -
            current
        ).total_seconds() / 3600

        quarter_energy = (
            avg_power *
            hours
        )

        lookup_time = current.replace(
            minute=(
                current.minute // 15
            ) * 15,
            second=0,
            microsecond=0
        )

        price = price_lookup.get(
            lookup_time
        )

        if price is not None:

            total_price = (
                engie_total_price(
                    price
                )
            )

            total_cost += (
                quarter_energy *
                total_price
            )

            total_energy += (
                quarter_energy
            )

        current = quarter_end

    if total_energy == 0:
        return (
            0.0,
            0.0
        )

    avg_price = (
        total_cost /
        total_energy
    )

    return (
        round(avg_price, 5),
        round(total_cost, 2)
    )