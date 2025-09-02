from dataclasses import dataclass, field

from math import prod
import constants

## This is the Standard Calculator Age model Module in my calculators. 
@dataclass
class new_Age:
    age: int
    q: list
    p: list = field(init=False)

    l: int = field(init=False)
    
    v: float  = field(init=False)

    d: float = field(init=False)
    n: float = field(init=False)
    
    constants: object = constants.Constatnts

 

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


