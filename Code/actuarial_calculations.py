from dataclasses import dataclass, field

import constants

import Age_constructor
import analyze_actuarial_data



@dataclass
class Calculate_actuarial_factors:
    q_csv: str
    
    age_data : list = field(init=False)
    

    
    def create_age_data(self):
        q_list = analyze_actuarial_data.Analyze_q_list(csv_file=self.q_csv).q_list
        age_data=[]
        i=0
        for value in q_list:
            age=Age_constructor.new_Age(i, q_list)
            age_data.append(age)
            i+=1
        return age_data
        
    def __post_init__(self):
        self.age_data = self.create_age_data()

@dataclass
class Calculate_simple_pension:
    q_csv: str
    age: int
    saldo: float
    k: float = field(init=False)
    pension: float = field(init=False)
    
    def get_data(self):
        data = Calculate_actuarial_factors(self.q_csv)
        k = 12 * ((data.age_data[self.age].n / data.age_data[self.age].d) - (11/24))
        print(k)
        return k
    
    def get_pension(self):
        return round(self.saldo/self.k ,2)
    
    def __post_init__(self):
        self.k=self.get_data()
        self.pension=self.get_pension()
    
@dataclass
class Calculate_guaranteed_pension:
    q_csv: str
    age: int
    saldo: float
    k: float = field(init=False)
    pension: float = field(init=False)
    
    def get_data(self):
        data = Calculate_actuarial_factors(self.q_csv)
        k = 12 * ((data.age_data[self.age].n / data.age_data[self.age].d) - (11/24))
        print(k)
        return k
    
    def get_pension(self):
        return round(self.saldo/self.k ,2)
    
    def __post_init__(self):
        self.k=self.get_data()
        self.pension=self.get_pension()

@dataclass
class Calculate_inheriatry_pension:
    pass

print(Calculate_simple_pension("Code\q_csv.csv",68,30000))