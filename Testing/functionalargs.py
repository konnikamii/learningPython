def foo(a, b, *args, **kwargs):  # these are parameters
    print(a, b)
    for arg in args:
        print(arg)
    for key in kwargs:
        print(key, kwargs[key])


# *args - as many positional param or args
# **kwargs - as many key word param or args

foo(1, 2, 3, 3, 4, sex=5, sieben=7)  # these are arguments

# Unpacking dict/list


def fo1(a, b, c):
    print(a, b, c)


mydict = {"a": 1, "b": 2, "c": 4}
mylist = [1, 3, 2]

fo1(*mylist)
fo1(**mydict)

# Local vs global variables


def fo2():
    global number  # need to state this to modify the global variable
    number = 3
    x = number
    print("number inside function is", x)


number = 0
fo2()
print(number)


###
def fo3():
    num = 3


num = 0
fo3()
print(num)  # here num still 0 cuz it cant be modded as local var in fo3


# Mutable vs immutable variables
def fo4(x):
    x = 5


var = 10
fo4(var)
print(var)  # here var is immutable int so cannot be changed like that


def fo5(a_list):
    # a_list = [2,3,4] now it wont work cuz it binds to local var
    a_list.append(4)
    a_list[0] = -100


my_list = [1, 2, 3]
fo5(my_list)
print(my_list)  # changes the global mutable object


def fo6(a_list):
    a_list += [22, 33, 44]  # this changes


my_list = [1, 2, 3]
fo6(my_list)
print(my_list)


def fo7(a_list):
    a_list = a_list + [22, 33, 44]  # this doesnt change


my_list = [1, 2, 3]
fo7(my_list)
print(my_list)
