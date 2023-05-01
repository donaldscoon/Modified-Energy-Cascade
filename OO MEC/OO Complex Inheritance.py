class Person:
    number_of_people = 0        # a class attribute this will not change person to person

    def __init__(self, name):
        self.name = name        # this can change person to person

    @classmethod
    def number_of_people(cls):
        return cls.number_of_people_
    
    @classmethod
    def add_person(cls):
        cls.number_of_people +=1

p1 = Person("Tim")
p2 = Person("Jill")
print(Person.number_of_people)
Person.number_of_people = 8     # that allows global modifications
print(p2.number_of_people)      # says 8 b/c the higher class says its 8