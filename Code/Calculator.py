from dataclasses import dataclass, field
from math import prod, floor
import csv
from scipy.stats import norm
import numpy as np

## Creates a new age object with all the actuarial factors calculated
@dataclass
class new_Age_Data:
    company: object
    q: list[float]
    
    age: list[int] = field(default_factory=lambda: [i for i in range(0, 101)])

    p: list[float] = field(init=False)

    l: list[int] = field(init=False)

    v: list[float] = field(init=False)

    d: list[float] = field(init=False)
    n: list[float] = field(init=False)

    ## Calculates l, v, d, n based on the age and q values
    
    def calculate_p(self):
        p = []
        for value in self.q:
            p.append(1 - value)
        return p

    def calculate_l(self):
        l = []
        for age in self.age:
            if age == 0:
                l.append(self.company.total_people)
            else:
                l.append(round(self.company.total_people * prod(self.p[:age])))
        return l

    def calculate_v(self):
        v = []
        for age in self.age:
            v.append((1 / (1 + self.company.interest))**age)
        return v

    def calculate_d(self):
        d = []
        for age in self.age:
            d.append(self.l[age] * self.v[age])
        return d

    def calculate_n(self):
        n = []
        for age in self.age:
            n.append(sum(self.d[age :]))
        return n
    
    def __post_init__(self):
        self.p = self.calculate_p()
        self.l = self.calculate_l()
        self.v = self.calculate_v()
        self.d = self.calculate_d()
        self.n = self.calculate_n()


# ----------------------------------------------------------------------------------------------------------------------
## Analyzes the q values from NSI and finds the mean and standard diviation of age of death
## Returns the q and p lists for further calculations
@dataclass
class Analyze_q_list:

    csv_file: csv
    company: object
    q_list: list = field(init=False)
    p_list: list = field(init=False)

    l_difference: list = field(init=False)

    age_of_death: list = field(init=False)
    smoothing_factor: int = 0

    mean: float = field(init=False)
    standard_diviation: float = field(init=False)

    
    ## Chains the data from NSI to a list
    def convert_csv_to_list(self):
        q_list = []
        p_list = []
        with open(self.csv_file, "r") as q_csv:
            example_q_list = csv.reader(q_csv)
            for row in example_q_list:
                q_list.append(float(row[0]))
                p_list.append(1 - float(row[0]))
        return [q_list, p_list]

    ## Model Deaths at Age on average, given the data
    def calculate_l_list(self):
        age = 0
        l_list = []
        l_difference = []
        p_product = 1
        while age < len(self.p_list):
            l_list.append(round(self.company.total_people * p_product))
            p_product *= self.p_list[age]
            age += 1
        i = 1
        while i < len(l_list):
            l_difference.append(l_list[i - 1] - l_list[i])
            i += 1
        return l_difference
    
    def find_parameters(self):
        ages = []
        age_of_death = []
        if self.smoothing_factor != 0:
            for i in range(len(self.l_difference) - self.smoothing_factor + 1):
                ages.append(
                    sum(self.l_difference[i : i + self.smoothing_factor])
                    / self.smoothing_factor
                )
        else:
            ages = self.l_difference
        j = 0
        for l in ages:
            i = 0
            while i < l:
                age_of_death.append(j)
                i += 1
            j += 1

        return age_of_death

    def plot_age_of_death(self):
            import matplotlib.pyplot as plt
            plt.hist(self.age_of_death, bins=30, density=True, alpha=0.6, color='g')
            plt.title(f'μ = {self.mean:.2f}, σ = {self.standard_diviation:.2f}')
            plt.xlabel('Age of Death')
            plt.ylabel('Density')
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, self.mean, self.standard_diviation)
            plt.plot(x, p, 'k', linewidth=2, label='Normal fit')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.show()  
    
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.fit.html#scipy.stats.rv_continuous.fit
        # https://www.probabilitycourse.com/chapter8/8_2_3_max_likelihood_estimation.php

    def __post_init__(self):
        self.q_list = self.convert_csv_to_list()[0]
        self.p_list = self.convert_csv_to_list()[1]
        self.l_difference = self.calculate_l_list()
        self.age_of_death = self.find_parameters()
        self.mean, self.standard_diviation = norm.fit(self.age_of_death)
        # self.plot_age_of_death() #plotting can be enabled here


# ----------------------------------------------------------------------------------------------------------------------
### Base Pension class
@dataclass
class Pension:
    q_csv: str
    age: int
    saldo: float 
    company: object
    data: list[object] = field(init=False)

    
    def create_age_data(self):
        return new_Age_Data(q=Analyze_q_list(csv_file=self.q_csv, company=self.company).q_list, company=self.company)
  
    
    def __post_init__(self):
        self.data = self.create_age_data()



## Simple Pension Calculator
@dataclass
class Simple_pension(Pension):
    k: float = field(init=False)
    pension: float = field(init=False)

    def get_k(self):
        k = 12 * ((self.data.n[self.age] / self.data.d[self.age]) - (11 / 24))
        return k

    def get_pension(self):
        return round(self.saldo / self.k, 2)

    def __post_init__(self):
        super().__post_init__()
        self.k = self.get_k()
        self.pension = self.get_pension()


## Guaranteed Pension Calculator
@dataclass
class Guaranteed_pension(Pension):
    guaranteed_period_years: int
    k: float = field(init=False)
    pension: float = field(init=False)

    def get_k(self):
        v=self.data.v[1]
        k = 12 * ((self.data.n[self.age + self.guaranteed_period_years]/ self.data.d[self.age])- ((11 / 24)* (self.data.d[self.age +self.guaranteed_period_years]/ self.data.d[self.age]))) + ((1-v**self.guaranteed_period_years)/(1-v**(1/12)))
        return k

    def get_pension(self):
        return round(self.saldo / self.k, 2)

    def __post_init__(self):
        super().__post_init__()
        self.k = self.get_k()
        self.pension = self.get_pension()


## Instalment Pension Calculator
@dataclass
class Instalment_pension(Pension):
    instalment_ammount: float
    instalment_period_months: int
    k: float = field(init=False)
    pension: float = field(init=False)

    def get_k(self):
        k = 12 * (
            self.data.n[floor((12*self.age + self.instalment_period_months) / 12)]
            / self.data.d[self.age]
            - (11 / 24)
            * self.data.d[floor((12*self.age + self.instalment_period_months) / 12)]
            / self.data.d[self.age]
        )
        return k

    def find_saldo_after_instalments(self):
        summ=0
        h=self.instalment_ammount
        v=self.data.v[1]
        i=0
        while i < self.instalment_period_months:
            summ+=h*v**(i/12)
            i+=1
        return self.saldo - summ
    
    def get_pension(self):
        return round(
            ((self.find_saldo_after_instalments()*(1-self.company.risk_level))
            / self.k),
            2)
        
    def __post_init__(self):
        super().__post_init__()
        self.k = self.get_k()
        self.pension = self.get_pension()

