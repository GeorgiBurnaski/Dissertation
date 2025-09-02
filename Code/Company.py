from dataclasses import dataclass 


@dataclass
class Company:
    pass


@dataclass
class Saglasie(Company):
    name: str = "Saglasie"
    r: float = 0.05
