from dataclasses import dataclass, field
import csv
import constants


from scipy.stats import norm

## This module is for functions connected with Mortality Calculations
## Converts: CSV Data to Mortality Array, Approximates mean and standart diviation of Normal Distribution, modeling the exaxt mortality.
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
    
    ## Chains the data from NSI.
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

        
    


