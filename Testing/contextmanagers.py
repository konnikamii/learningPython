# method 1 better!
with open("notes.txt", "w") as file:
    file.write("some todo..")


# method 2
file = open("notes.txt", "w")
try:
    file.write("some todo...")
finally:
    file.close()


# locks

from threading import Lock

lock = Lock()

lock.acquire()
# ///
lock.release()

# Or..

# with lock:
# ----
# no need for release its auto


class ManagedFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print("enter")
        self.file = open(self.filename, "w")
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file:
            self.file.close()
        if exc_type is not None:
            print("exception handled")
        # print("exc:", exc_type, exc_value)
        print("exit")
        return True


with ManagedFile("notes.txt") as file:
    print("do some stuf/")
    file.write("some todo/")
    file.somemethod()
print("continuing")


# do as function
from contextlib import contextmanager


@contextmanager
def open_managed_file(filename):
    f = open(filename, "w")
    try:
        yield f
    finally:
        f.close()


with open_managed_file("notes.txt") as f:
    f.write("some to doooooo")
