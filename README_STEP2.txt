Stap 2
1. Kopieer de bestanden naar je projectmap en overschrijf bestaande bestanden.
2. Open PowerShell in de projectmap.
3. Zet tijdelijk je wachtwoord als environment variable:
   $env:ALPHAESS_PASSWORD="jouw_wachtwoord"
4. Run:
   python scripts\session_sync.py
5. Controleer of data/charging_history.db aangemaakt wordt en sessies geladen worden.
