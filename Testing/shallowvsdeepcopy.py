import copy

org = [0, 1, 2, 3, 4]
cpy = org
cpy[0] = -10
print(cpy)
print(org)  # doesnt work

org = [0, 1, 2, 3, 4]
cpy = copy.copy(org)
# cpy = list(org)
# cpy = org[:]
# cpy = org.copy()
cpy[0] = -10
print(cpy)
print(org)  # shallow copy 1 lvl deep

org = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
cpy = copy.copy(org)
cpy[0][1] = -10
print(cpy)
print(org)  # shallow copy 1 lvl deep doesnt work here


org = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
cpy = copy.deepcopy(org)
cpy[0][1] = -10
print(cpy)
print(org)  # deep copy works


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Company:
    def __init__(self, boss, employee):
        self.boss = boss
        self.employee = employee


p1 = Person("Alex", 27)
p2 = copy.copy(p1)  # shallow copy
p2.age = 28
print(p2.age)
print(p1.age)

p3 = Person("Joe", 55)
company = Company(p1, p3)
compclone = copy.deepcopy(company)  # deep copy
compclone.boss.age = 58
print(compclone.boss.age)
print(company.boss.age)
