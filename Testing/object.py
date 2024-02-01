class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    def add(self, x):
        return x + 1

    def bark(self):
        print("bark")


d = Dog("alex", 23)
print(d.name)
d2 = Dog("alex2", 12)
print(d2.name)
d.set_age(22)
print(d.age)
d.bark()
print(d.add(5))
print(type(d))


###############
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def get_grade(self):
        return self.grade


class Course:
    def __init__(self, name, max_students):
        self.name = name
        self.max_students = max_students
        self.students = []

    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student)
            return True
        return False

    def get_average_grade(self):
        value = 0
        for student in self.students:
            value += student.get_grade()

        return value / len(self.students)


s1 = Student("Tim", 19, 96)
s2 = Student("Bil", 15, 85)
s3 = Student("Jill", 12, 75)

course = Course("Science", 2)
course.add_student(s1)
course.add_student(s2)

print(course.get_average_grade())
#####################


class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(f"I am {self.name} and I am {self.age} years old")

    def speak(self):
        print("I dont know what to say")


class Cat(Pet):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def speak(self):
        print("Meow")

    def show(self):
        print(f"I am {self.name} and I am {self.age} years old and i am {self.color}")


class Doggo(Pet):
    def speak(self):
        print("Bark")


class Fish(Pet):
    pass


p = Pet("Tim", 19)
p.show()
c = Cat("Bill", 23, "brown")
c.show()
d = Doggo("Jill", 223)
d.speak()
f = Fish("bubbles", 10)
f.speak()

######Class attributes and class methods


class Person:
    number_of_people = 0

    def __init__(self, name):
        self.name = name
        # Person.number_of_people += 1
        Person.add_person()

    @classmethod
    def number_of_people_(cls):
        return cls.number_of_people

    @classmethod
    def add_person(cls):
        cls.number_of_people += 1


p1 = Person("tim")
print(Person.number_of_people)
p2 = Person("timy")
print(Person.number_of_people)

print(Person.number_of_people_())

###### Static methods


class Math:
    @staticmethod
    def add5(x):
        return x + 5

    @staticmethod
    def add10(x):
        return x + 10

    @staticmethod
    def pr():
        print("run")


print(Math.add5(4))
print(Math.add10(2))
Math.pr()
