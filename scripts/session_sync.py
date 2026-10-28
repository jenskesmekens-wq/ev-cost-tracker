from datetime import datetime
import sqlite3, yaml, os
from alphaess_client import AlphaESSClient
from logger import logger

CONFIG='config.yaml'
START_DATE=datetime(2026,10,15)

def load_config():
    with open(CONFIG,'r',encoding='utf-8') as f: return yaml.safe_load(f)

def main():
    cfg=load_config()
    email=os.getenv('ALPHAESS_EMAIL',cfg['alphaess']['email'])
    password=os.getenv('ALPHAESS_PASSWORD','')
    client=AlphaESSClient(email,password)
    client.login()
    sessions=client.get_charging_sessions(cfg['system']['sys_sn'],cfg['system']['charger_sn'])
    conn=sqlite3.connect(cfg['database']['path'])
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY,start_time TEXT UNIQUE,end_time TEXT,kwh REAL)')
    newcount=0
    for s in sessions:
      st=datetime.fromisoformat(s['beginDate'].replace(' ','T'))
      if st<START_DATE: continue
      c.execute('INSERT OR IGNORE INTO sessions(start_time,end_time,kwh) VALUES(?,?,?)',(s['beginDate'],s['endDate'],s['chargingCapacity']))
      if c.rowcount: newcount+=1
    conn.commit()
    print(f'Sessies opgehaald: {len(sessions)}')
    print(f'Nieuwe sessies: {newcount}')

if __name__=='__main__': main()
