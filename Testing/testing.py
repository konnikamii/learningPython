from functools import *


def students():
    D = {}
    while True:
        studenid = input("ID: ")
        grades = input("Grades: ")
        endloop = input("write no if finished otherwise ENTER")
        if studenid in D:
            print("student already in")
        else:
            D[studenid] = grades.split(",")
        if endloop == "no":
            return D


data = students()
# data = {2: [1, 2, 3, 4, 5, 5], 5: [5, 4, 8, 4]}


for i in data:
    print(f"studen {i} grades {data[i]}")
print(data)

"""
sum = 0
for j in data:
    print(f"Student {j} has the following grades: {data[j]}")
    for i in data[j]:
        sum += i
print(sum / len(data[j]))

from statistics import mean
"""


def avggrades(dic):
    avgmark = {}
    if len(dic) == 0:
        print("Dic empty")
    else:
        for x in dic:
            l = dic[x]
            s = 0
            for marks in l:
                s += float(marks)
            avgmark[x] = round(s / len(l), 2)
        return avgmark


avg = avggrades(data)
print(avg)

"""
StudentGrades = {
    "Ivan": [4.32, 3, 2],
    "Martin": [3.45, 5, 6],
    "Stoyan": [2, 5.67, 4],
    "Vladimir": [5.63, 4.67, 6],
}

for st, vals in StudentGrades.items():
    print("Average for {} is {}".format(st, mean(vals)))
"""
