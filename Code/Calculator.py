from dataclasses import dataclass, field
from math import prod
import csv
from scipy.stats import norm

import constants

## Creates a new age object with all the actuarial factors calculated
@dataclass
class new_Age:
    age: int
    q: list[float]
    p: list[float]  = field(init=False)

    l: int = field(init=False)
    
    v: float  = field(init=False)

    d: float = field(init=False)
    n: float = field(init=False)
    
    constants: object = constants.Constatnts
    
    ## Calculates l, v, d, n based on the age and q values

    def calculate_l (self):
        if self.age==0:
            self.l=self.constants.total_people
        else: 
            self.l=self.constants.total_people * prod(self.p[:self.age-1])
        return round(self.l)
        
    def calculate_v (self):
        self.v=(1/(1+ self.constants.i))**self.age
        return self.v
    
    def calculate_d(self):
        self.d=self.l*self.v
        return self.d
    
    def calculate_n(self):
        i=0
        n=0
        total_d=0
        currnet_d=0
        while i<101:
            total_d+=self.d
            i+=1
            
        while n<self.age:
            currnet_d+=self.d
            n+=1

        return total_d-currnet_d
    
    def __post_init__(self):
        p=[]
        for value in self.q:
            p.append(1-value)
        self.p=p
        self.l = self.calculate_l()
        self.v=self.calculate_v()
        self.d=self.calculate_d()
        self.n=self.calculate_n()

## Analyzes the q values from NSI and finds the mean and standard diviation of age of death
## Returns the q and p lists for further calculations
@dataclass        
class Analyze_q_list: 
    
    csv_file: csv
    
    q_list: list = field(init=False)
    p_list: list = field(init=False)
    
    l_difference: list = field(init=False)
    
    age_of_death: list = field(init=False)
    smoothing_factor: int = 0
    
    mean: float = field(init=False)
    standard_diviation: float = field(init=False)
  
    constants: object = constants.Constatnts
    
    ## Chains the data from NSI to a list
    def convert_csv_to_list(self):
        q_list=[]
        p_list=[]
        with open(self.csv_file,'r') as q_csv:
            example_q_list=csv.reader(q_csv)
            for row in example_q_list:
                q_list.append(float(row[0]))
                p_list.append(1-float(row[0]))
        return [q_list, p_list]
    
    ## Model Deaths at Age on average, given the data
    def calculate_l_list(self):
        age = 0
        l_list=[]
        l_difference=[]
        p_product = 1
        while age<len(self.p_list):
            l_list.append(round(self.constants.total_people * p_product))  
            p_product *= self.p_list[age]
            age+=1
        i=1
        while i<len(l_list):
            l_difference.append(l_list[i-1]-l_list[i])
            i+=1
        return l_difference
    
    def find_parameters(self):
        ages=[]
        age_of_death=[]
        if self.smoothing_factor!=0:  
            for i in range(len(self.l_difference)-self.smoothing_factor + 1):
                ages.append(sum(self.l_difference[i:i+self.smoothing_factor])/self.smoothing_factor)
        else:
            ages=self.l_difference
        j=0
        for l in ages:
            i=0
            while i<l:
                age_of_death.append(j)
                i+=1
            j+=1

        return age_of_death    
                
                # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.fit.html#scipy.stats.rv_continuous.fit
                # https://www.probabilitycourse.com/chapter8/8_2_3_max_likelihood_estimation.php            

    
    def __post_init__(self):
        self.q_list = self.convert_csv_to_list()[0]
        self.p_list = self.convert_csv_to_list()[1]
        self.l_difference=self.calculate_l_list()
        self.age_of_death = self.find_parameters()
        self.mean, self.standard_diviation = norm.fit(self.age_of_death)

## Calculates the actuarial factors for all ages based on the q values
@dataclass
class Calculate_actuarial_factors:
    q_csv: str
    
    age_data : list [object] = field(init=False)
    

    
    def create_age_data(self):
        q_list = analyze_actuarial_data.Analyze_q_list(csv_file=self.q_csv).q_list
        age_data=[]
        i=0
        for value in q_list:
            age_data.append(new_Age(i, q_list))
            i+=1
        return age_data
        
    def __post_init__(self):
        self.age_data = self.create_age_data()


## Simple Pension Calculator  
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

## Guaranteed Pension Calculator   
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

## Inheriatry Pension Calculator 
@dataclass
class Calculate_inheriatry_pension:
    pass

print(Calculate_simple_pension("Code\q_csv.csv",68,30000))