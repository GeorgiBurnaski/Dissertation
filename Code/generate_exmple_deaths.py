from dataclasses import dataclass, field

import random


@dataclass  
class Generate_deaths:
    constants: object
    q_list: list = field(init=False)

    
    def generate_normal_distribution(self):
        q=0
        q_list=[]
        
        life_list=[]
        total_deaths_age=[]
        
        i=0
        while i<self.constants.total_people:
            life_list.append(round(random.gauss(self.constants.mu, self.constants.d)))
            i+=1
        
        i=0
        while i<100:
            total_deaths_age.append(life_list.count(i))
            i+=1
            
        total_people=self.constants.total_people    
        i=0
        while i<len(total_deaths_age):
            q=total_deaths_age[i]/total_people
            total_people-=total_deaths_age[i]
            q_list.append(q)
            i+=1
            
        return q_list     
    
    def __post_init__(self):
        self.q_list=self.generate_normal_distribution()