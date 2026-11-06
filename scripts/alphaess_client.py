import requests


LOGIN_URL = (
    "https://platform-eur.alphaess.com"
    "/api/users-center/sessions"
)

REPORT_URL = (
    "https://platform-eur.alphaess.com"
    "/api/internal/v1/ev-charger/report"
)

SITE_ID = "zq6x3eLCpVvbrcEbnLF"


class AlphaESSClient:

    def __init__(
        self,
        email,
        password
    ):

        self.email = email
        self.password = password
        self.token = None

    def login(self):

        payload = {
            "email": self.email,
            "type": "password",
            "password": self.password
        }

        r = requests.post(
            LOGIN_URL,
            json=payload,
            timeout=30
        )
	
        print()
        print("STATUS:", r.status_code)
        print()
        print("RESPONSE:")
        print(r.text)
        print()


        r.raise_for_status()

        if not r.text.strip():

            raise RuntimeError(
                "Lege login response van AlphaESS."
            )

        try:

            data = r.json()

        except Exception:

            raise RuntimeError(
                f"Ongeldige login response "
                f"van AlphaESS:\n\n"
                f"{r.text[:500]}"
            )

        if "accessToken" not in data:

            raise RuntimeError(
                f"Geen accessToken ontvangen:\n\n"
                f"{data}"
            )

        self.token = data["accessToken"]

        return self.token

    def headers(self):

        return {
            "Authorization":
            f"Bearer {self.token}"
        }

    def get_charging_sessions(
        self,
        sys_sn,
        charger_sn
    ):

        r = requests.get(
            REPORT_URL,
            headers=self.headers(),
            params={
                "pageNum": 1,
                "pageSize": 500,
                "sysSn": sys_sn,
                "chargingPileSn": charger_sn
            },
            timeout=30
        )

        r.raise_for_status()

        if not r.text.strip():

            print()
            print(
                "Waarschuwing: lege "
                "charging sessions response."
            )
            print()

            return []

        try:

            data = r.json()

        except Exception:

            print()
            print(
                "Waarschuwing: ongeldige "
                "charging sessions JSON."
            )
            print(
                r.text[:500]
            )
            print()

            return []

        return data.get(
            "list",
            []
        )

    def get_power_history(
        self,
        begin_datetime,
        end_datetime,
        interval=5
    ):

        url = (
            "https://platform-eur.alphaess.com"
            f"/api/internal/v1/sites/"
            f"{SITE_ID}/power"
        )

        r = requests.get(
            url,
            headers=self.headers(),
            params={
                "beginDateTime":
                begin_datetime,

                "endDateTime":
                end_datetime,

                "interval":
                interval
            },
            timeout=60
        )

        r.raise_for_status()

        if not r.text.strip():

            print()
            print(
                "Waarschuwing: lege "
                "power history response."
            )
            print()

            return {}

        try:

            return r.json()

        except Exception:

            print()
            print(
                "Waarschuwing: ongeldige "
                "power history JSON."
            )
            print(
                r.text[:500]
            )
            print()

            return {}