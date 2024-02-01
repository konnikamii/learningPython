import functools
from typing import Any

print("\n Decorator without arguments:")
## Decorator without arguments


def start_end_decorator(func):
    def wrapper():
        print("Start")
        func()
        print("End")

    return wrapper


@start_end_decorator
def print_name():
    print("Phil")


# print_name = start_end_decorator(print_name)

print_name()


print("\n Decorator with arguments:")


### Decorator with arguments
print("\n -- Addition:")


# 1
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Do before..
        print("Hello")
        result = func(*args, **kwargs)
        # Do after...
        print("Bye")
        return result

    return wrapper


@my_decorator
def add5(x):
    return x + 5


print(add5(2))

print("\n -- Repeating function n times:")


# 2
def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator_repeat


@repeat(num_times=2)
def greet(name):
    print(f"Hello {name}")


greet("alexi")


print("\n Multiple decorators:")
## Multiple decorators


def startend_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Do before..
        print("Start")

        result = func(*args, **kwargs)

        # Do after...
        print("End")
        return result

    return wrapper


def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {result!r}")
        return result

    return wrapper


@debug
@startend_decorator
def say_hello(name):
    greeting = f"Hello {name}"
    print(greeting)
    return greeting


say_hello("Philip")


print("\n Class decorator:")
## Class decorator


class CountCalls:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"This is executed {self.num_calls} times")
        return self.func(*args, **kwargs)


@CountCalls
def hello():
    print("Hello")


hello()
hello()
