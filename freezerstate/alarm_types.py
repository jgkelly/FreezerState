from enum import Enum

class AlarmTypes(Enum):
    Normal = None
    High = 1
    Low = 2
    StatusUpdate = 3