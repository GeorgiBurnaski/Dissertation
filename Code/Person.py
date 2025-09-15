from dataclasses import dataclass,field
from datetime import datetime

@dataclass
class Person:
    name: str
    egn: int  # Unique identifier
    income: float  # Monthly income
    savings: float  # Current savings
    
    sex: str  =field(init=False) # 'M' or 'F'
    
    age_years: int = field(init=False)  # Age in years, to be calculated
    age_months: int = field(init=False)  # Age in months, to be calculated
    
    months_to_retirement: int = field(init=False)  # Months left to retirement, to be calculated
    years_to_retirement: int = field(init=False)  # Years left to retirement, to be calculated
    retirement_age: int = field(init=False)  # Default retirement age
    
    
    def calculate_age(self):
        today = datetime.today()
        birth_year = self.egn.tostring()[:2]
        if int(birth_year) <= int(str(today.year)[2:]):
            birth_year = 2000 + int(birth_year)
        else:
            birth_year = 1900 + int(birth_year)
        print(birth_year)
        birth_month = self.egn.tostring()[2:4]
        birth_month = int(birth_month)
        if birth_month > 40:
            birth_month -= 40
        birth_day = self.egn.tostring()[4:6]
        birth_day = int(birth_day)
        birth_date = datetime(birth_year, birth_month, birth_day)
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        age_months = today.month - birth_date.month - (today.day < birth_date.day)
        if today.day < birth_date.day:
            age_months -= 1
        if age_months < 0:
            age_months += 12
        return age_years, age_months

    def determine_sex(self):
        if int(str(self.egn)[-1]) % 2 == 0:
            return 'F'
        else:
            return 'M'
        
    def determine_retirement_age(self):
        current_year = datetime.now().year
        pension_ages = {
            'M': {2024: 64, 2025: 64, 2026: 64, 2027: 64, 2028: 64, 2029: 66, 2030: 67, 2031: 67, 2032: 68, 2033: 68, 2034: 69, 2035: 69, 2036: 70},
            'F': {2024: 62, 2025: 62, 2026: 62, 2027: 62, 2028: 62, 2029: 63, 2030: 63, 2031: 63, 2032: 63, 2033: 64, 2034: 64, 2035: 64, 2036: 65}}
        pension_months={
            'M':{2025:8,2026:9,2027:10,2028:11,2029:0,2030:0,2031:0,2032:0,2033:0,2034:0,2035:0,2036:0},
            'F':{2025:4,2026:6,2027:8,2028:10,2029:0,2030:3,2031:6,2032:9,2033:0,2034:3,2035:6,2036:69}}
        if current_year >= 2037:
            pension_ages={
                'M': 65,
                'F': 65}
            pension_months={
                'M': 0,
                'F': 0}
        else:
            pension_ages={
                'M': pension_ages['M'][current_year],
                'F': pension_ages['F'][current_year]}
            pension_months={
                'M': pension_months['M'][current_year],
                'F': pension_months['F'][current_year]}
        return pension_ages, pension_months

    def calculate_birth_date_for_retirement(self):
        pension_ages, pension_months = self.determine_retirement_age()
        age_years, age_months = self.calculate_age()
        
    
    def _post_init__(self):
        pass