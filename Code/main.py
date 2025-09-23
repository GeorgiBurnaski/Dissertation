from Company import Company
from Person import Person
from Calculator import Simple_pension, Guaranteed_pension, Instalment_pension


my_company = Company(name="Sagalsie", interest=0.075, risk_level=0.015, fund_data="Code/Data/Saglasie_fund_actives.csv")

me = Person(name="Georgi", egn=9606067062, income=2000, savings=10000)

my_company.add_person(me)

georgi = next(person for person in my_company.people if person.name == 'Georgi')



print(Simple_pension(
    q_csv="Code/Data/NSI_q_values.csv",
    age=65,
    saldo=georgi.funds_at_retirement,
    company=my_company
).pension)

print(
    Guaranteed_pension(
        q_csv="Code/Data/NSI_q_values.csv",
        age=65,
        saldo=georgi.funds_at_retirement,
        company=my_company,
        guaranteed_period_years=10,
    ).pension
)

print(
    Instalment_pension(
        q_csv="Code/Data/NSI_q_values.csv",
        age=65,
        saldo=georgi.funds_at_retirement,
        instalment_ammount=400,
        instalment_period_months=15*12,
        company=my_company,
    ).pension
)





