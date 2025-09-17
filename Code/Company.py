from dataclasses import dataclass 
from Person import Person

@dataclass
class Company:
    name: str
    interest: float  # Annual interest rate as a decimal (e.g., 0.05 for 5%)
    risk_level: float  # Risk level as a decimal
    fund_data: str  # Path to fund data CSV file
    people: list = None  # List of Person objects associated with the company
    
    total_people: int = 100000  # Total number of people for actuarial calculations
    
    def add_person(self, person):
        if self.people is None:
            self.people = []
        self.people.append(person)
