from dataclasses import dataclass,field
from datetime import datetime, timedelta
from Finances import Finances
@dataclass
class Person:
    name: str
    egn: int  # Unique identifier
    income: float  # Monthly income
    savings: float  # Current savings
    
    sex: str  =field(init=False) # 'M' or 'F'
    age: datetime = field(init=False)  # Age as a datetime object
    years: int = field(init=False)  # Age in years
    months: int = field(init=False)  # Additional months beyond full years

    retirement_age: timedelta = timedelta(days=65*365.25)  # Default retirement age
    months_to_retirement: int = field(init=False)  # Months until retirement
    
    funds_at_retirement: float = field(init=False)  # Estimated funds at retirement

    today = datetime.today()
    
    def calculate_age(self):

        birth_year = str(self.egn)[:2]
        if int(birth_year) <= int(str(self.today.year)[2:]):
            birth_year = 2000 + int(birth_year)
        else:
            birth_year = 1900 + int(birth_year)

        birth_month = str(self.egn)[2:4]
        birth_month = int(birth_month)
        if birth_month > 40:
            birth_month -= 40
        birth_day = str(self.egn)[4:6]
        birth_day = int(birth_day)
        birth_date = datetime(birth_year, birth_month, birth_day)
        
        if self.today.month < birth_month or (self.today.month == birth_month and self.today.day < birth_day):
            years = self.today.year - birth_date.year - 1
        else:
            years = self.today.year - birth_date.year
        
        if self.today.day < birth_day:
            months = (self.today.month - birth_month - 1) % 12
        else:
            months = (self.today.month - birth_month) % 12
        
        age = self.today - birth_date

        return age, years, months
    
    
    def determine_sex(self):
        if int(str(self.egn)[-2]) % 2 == 0:
            return 'M'
        else:
            return 'F'
    
    def calculate_months_to_retirement(self):
        if self.age>=self.retirement_age:
            return 0
        else:
            return int((self.retirement_age - self.age).days // 30.44)  # Approximate month length
        
    def funds_at_retirement_basic(self):
        if self.months_to_retirement <= 0:
            return self.savings
        else:
            return self.savings + self.income * self.months_to_retirement * 0.05  # Simplified calculation
    
    def funds_at_retirement_after_simulation(self,):
        if self.months_to_retirement <= 0:
            return self.savings
        else:
            finance_simulation = Finances(csv_path="Code/Data/Saglasie_fund_actives.csv", days_to_predict=self.months_to_retirement*30)
            return finance_simulation.calculate_complex_asset_for_UPF(collected_amount=self.savings, added_amount=self.income*0.05/30.44)
          
    def __post_init__(self):
        self.age, self.years, self.months = self.calculate_age()
        self.sex = self.determine_sex()
        self.months_to_retirement = self.calculate_months_to_retirement()
        self.funds_at_retirement = self.funds_at_retirement_after_simulation()
        
