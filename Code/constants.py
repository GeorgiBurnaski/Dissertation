
from dataclasses import dataclass

@dataclass
class Constatnts:
    total_people: int = 100000
    example_age: int = 58
    total_funds: float = 10000

    i: float = 0.037
    
    #These values are taken from MLE of gausian curve fit of the data in NSI
    mu: float = 74.94
    d: float = 15.52

        








