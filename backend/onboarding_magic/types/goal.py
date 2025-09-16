from enum import Enum

class Goal(Enum):
    MUSCLE_GAIN_RECOMP = "muscle_gain_recomp" # fat loss implied
    MUSCLE_RETAIN_RECOMP = "muscle_retain_recomp" # fat loss implied
    MAINTAIN = "maintain" # retain muscle and fat as is

    def __str__(self):
        return self.value
