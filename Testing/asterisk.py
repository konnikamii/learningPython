result = 5 * 9
print(result)

result = 2**4
print(result)  # =2^4

zeros = [0, 1] * 5
print(zeros)


def foo(a, b, *args, **kwargs):
    print(a, b)
    for arg in args:
        print(arg)
    for key in kwargs:
        print(key, kwargs[key])


def foo(a, b, *, c):  # enforces kwargs after *
    print(a, b, c)


def foo(a, b, c):
    print(a, b, c)


lista = [1, 2, 3]
foo(*lista)  # ** for dictionary

# unpacking containers
numbers = [1, 2, 3, 4, 5, 6]
beginning, *middle, secondlast, last = numbers
print(beginning)
print(middle)
print(secondlast)
print(last)

mtup = (1, 2, 3)
mlist = [4, 5, 6]
mset = {7, 8, 9}

newlist = [*mtup, *mlist, *mset]
print(newlist)

d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
d3 = {**d1, **d2}
print(d3)
