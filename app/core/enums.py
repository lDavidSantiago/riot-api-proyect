from enum import Enum

class MatchType(str, Enum):
    RANKED = "ranked"
    NORMAL = "normal"
    TOURNEY = "tourney"
