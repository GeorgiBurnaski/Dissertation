from dataclasses import dataclass 
from Finances import Finances


@dataclass
class Company:
    name: str
    interest: float  # Annual interest rate as a decimal (e.g., 0.05 for 5%)
    risk_level: float  # Risk level as a decimal
    fund_data: str  # Path to fund data CSV file
    people: list = None  # List of Person objects associated with the company
    
    def add_person(self, person):
        if self.people is None:
            self.people = []
        self.people.append(person)



