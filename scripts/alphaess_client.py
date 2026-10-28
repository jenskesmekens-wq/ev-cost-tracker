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

        r.raise_for_status()

        self.token = (
            r.json()["accessToken"]
        )

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

        data = r.json()

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
            f"https://platform-eur.alphaess.com"
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

        return r.json()