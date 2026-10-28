import requests
LOGIN_URL="https://platform-eur.alphaess.com/api/users-center/sessions"
REPORT_URL="https://platform-eur.alphaess.com/api/internal/v1/ev-charger/report"
class AlphaESSClient:
    def __init__(self,email,password): self.email=email; self.password=password; self.token=None
    def login(self):
      r=requests.post(LOGIN_URL,json={"email":self.email,"type":"password","password":self.password},timeout=30)
      r.raise_for_status(); self.token=r.json()['accessToken']; return self.token
    def headers(self): return {"Authorization":f"Bearer {self.token}"}
    def get_charging_sessions(self,sys_sn,charger_sn):
      r=requests.get(REPORT_URL,headers=self.headers(),params={"pageNum":1,"pageSize":500,"sysSn":sys_sn,"chargingPileSn":charger_sn},timeout=30)
      r.raise_for_status(); data=r.json(); return data.get('list',[])
