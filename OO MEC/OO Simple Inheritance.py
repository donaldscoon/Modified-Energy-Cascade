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
    def __init__(self, name, age, color):
        super().__init__(name,age)      # this allows us to reuse the stuff from the above portion and add color
        self.color = color

    def show(self):                     # new one to reflect the addition of color
        print(f"I am {self.name} and I am {self.age} years old, and I am {self.color}")

    def speak(self):        # this speak overwrites the inherited speak
        print("Meow")

class Dog(Pet): 
    def speak(self):
        print("Bark")

class Fish(Pet):            # will use inherited speak since there is none provided here
    pass

p = Pet("Tim", 19)
p.speak()
c = Cat("Bill", 34, "Brown") 
c.show()
d = Dog("Jill", 25)
d.speak()
f = Fish("Bubbles", 10)
f.speak()

