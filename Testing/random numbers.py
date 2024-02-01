print("Random module:")
import random

random.seed(1)  # set seed to allow same results
a = random.random()
print(a)  # random float

a = random.uniform(1, 10)
print(a)  # random float in range

a = random.randint(1, 10)
print(a)  # random int in range *included

a = random.randrange(1, 10)
print(a)  # random int in range *not included

a = random.normalvariate(0, 1)
print(a)  # random value from normal distribution with mean 0 and sd 1

mylist = list("ABCDEFGH")
print(mylist)
a = random.choice(mylist)
print(a)  # random choice
a = random.sample(mylist, 3)
print(a)  # no repetition
a = random.choices(mylist, k=3)
print(a)  # repetition
random.shuffle(mylist)
print(mylist)  # random shuffle


###############################
print("\n Secrets module:")
import secrets

# used for passwords not reproducable
a = secrets.randbelow(10)
print(a)  # rand int from 0-10 upper bound excluded
a = secrets.randbits(4)
print(a)  # rand int from binary 1111(=2^3+2^2+2^1+2^0=15),1011,etc
mylist = list("ABCDEFGH")
a = secrets.choice(mylist)
print(a)  # rand choice from list


#########################
print("\n Numpy module:")
import numpy as np

np.random.seed(4)
a = np.random.rand(3, 3)
print(a)  # array 3x3

a = np.random.randint(0, 7, (3, 4))
print("\n", a, "\n")  # array 3x4 with int from 0-7 excl

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr, "\n")
np.random.shuffle(arr)
print(arr)  # shuffles elements along 1st axis
