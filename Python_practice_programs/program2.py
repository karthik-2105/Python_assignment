from abc import ABC, abstractmethod

# Abstract base class
class Person(ABC):
    @abstractmethod
    def get_gender(self):
        pass


# Male class inheriting from Person
class Male(Person):
    def get_gender(self):
        print("Male")


# Female class inheriting from Person
class Female(Person):
    def get_gender(self):
        print("Female")


# Testing the functionality
if __name__ == "__main__":
    try:
        p = Person()  # This will raise an error because Person is abstract
        p.get_gender()
    except TypeError as e:
        print("Error:", e)

    m = Male()
    f = Female()

    m.get_gender()  # Output: Male
    f.get_gender()  # Output: Female
