from dataclasses import dataclass
@dataclass
class ChargingSession:
    start_time:str
    end_time:str
    kwh:float
