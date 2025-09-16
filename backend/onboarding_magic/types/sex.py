from enum import Enum

class Sex(Enum):
    MALE = "male"
    FEMALE = "female"

    def __str__(self):
        return self.value
