"""Inheritance: How can we avoid duplicating code. 
    Dog and cat share name and age. They inherit that info
    from a higher class. Done instead of def __init__(self, name, age) """
class Pet:
     def __init__(self, name, age):
        self.name = name
        self.age = age

     def show(self):
        print(f"I am {self.name} and I am {self.age} years old")

     def speak(self):
         print("IDK What to say yet")

class Cat(Pet):             # the pet in parens is the inheritance
    def speak(self):        # this speak overwrites the inherited speak
        print("Meow")

class Dog(Pet): 
    def speak(self):
        print("Bark")

class Fish(Pet):            # will use inherited speak since there is none provided here
    pass

p = Pet("Tim", 19)
p.speak()
c = Cat("Bill", 34)         # see? this Cat method used show without it being defined in cat
c.speak()
d = Dog("Jill", 25)
d.speak()
f = Fish("Bubbles", 10)
f.speak()

