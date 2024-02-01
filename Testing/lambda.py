add10 = lambda x: x + 10
print(add10(5))


def add10_f(x):
    return x + 10


print(add10_f(5))

mult = lambda x, y: x * y
print(mult(2, 4))

# sorted method
points2d = [(1, 2), (15, 1), (5, -1), (10, 4)]
points2d_sorted = sorted(
    points2d, key=lambda x: x[1]
)  # here lambda sorts by y argument
# lambda x: x[0]+x[1] would sort by sum of arguments

print(points2d)
print(points2d_sorted)

# map(func,seq)
a = [1, 2, 3, 4, 5]
b = map(lambda x: x * 2, a)
print(list(b))

## list comprehension
c = [x * 2 for x in a]
print(c)

# filter(func,seq)
a = [1, 2, 3, 4, 5, 6]
b = filter(lambda x: x % 2 == 0, a)
print(list(b))

##list comprehension
c = [x for x in a if x % 2 == 0]
print(c)

# reduce(func,seq)
from functools import reduce

product_a = reduce(lambda x, y: x * y, a)
print(product_a)
