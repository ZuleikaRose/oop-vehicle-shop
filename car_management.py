# Exercise: Car Management System

# In this exercise, you'll create a Python class called `Car` to manage a collection of cars in a terminal-based application. The goal is to practice using class and instance methods, while also understanding the distinction between them.

# ## Step 0: Class Definition

# Create a class named `Car` with the following attributes:

# - `all_cars` (class attribute): A list/dictionary that will store all the car instances created.
# - `total_cars` (class attribute): An integer that will keep track of the total number of cars.

# Implement the constructor `__init__` method to initialize the instance attributes:

# - `_id` (instance attribute): An integer that should never be repeated and only rise with each car instance
# - `_make` (instance attribute): A string representing the make of the car.
# - `_model` (instance attribute): A string representing the model of the car.
# - `_year` (instance attribute): An integer representing the manufacturing year of the car.
# - `_mileage` (instance attribute): An integer representing the vehicles total mileage
# - `_services` (instance attribute): A list that will store the services done to the car.

# ## Step 1: Terminal Application

# Create a terminal application to interact with your Car class. For each option in the menu provided, utilize class and instance attributes and instance methods to run your terminal program as expected. Use Python built in methods such as `input` to allow the user to input data through the terminal.

# ```bash
# ----  WELCOME  ----
# 1. Add a car
# 2. View all cars
# 3. View total number of cars
# 4. See a car's details
# 5. Service a car
# 6. Update mileage
# 7. Quit
# ```

# ### Conclusion

# This exercise offers hands-on experience in using class and instance methods to create a car management system. You've practiced distinguishing between methods that operate at the class level and those that operate at the instance level. By working on this exercise, you'll reinforce your understanding of these concepts and their practical application in object-oriented programming.

# As always, ensure that you follow good coding practices, such as using meaningful variable names, writing clear comments, and maintaining proper indentation. Happy coding!


class Car:
    # ---- Class attributes (shared by every Car) ----
    all_cars = {}      # maps car id -> Car instance
    total_cars = 0     # how many cars currently exist
    _next_id = 1       # ids only ever go up and are never reused

    def __init__(self, make, model, year, mileage):
        # ---- Instance attributes (unique to each car) ----
        self._id = Car._next_id
        self._make = make
        self._model = model
        self._year = year
        self._mileage = mileage
        self._services = []

        # Register this car at the class level
        Car._next_id += 1
        Car.all_cars[self._id] = self
        Car.total_cars += 1

    # Read-only public access to the private id
    @property
    def id(self):
        return self._id

    # ---- Class methods: act on the whole collection ----
    @classmethod
    def get_all_cars(cls):
        return list(cls.all_cars.values())

    @classmethod
    def get_total_cars(cls):
        return cls.total_cars

    @classmethod
    def find_car(cls, car_id):
        return cls.all_cars.get(car_id)

    # ---- Instance methods: act on one car ----
    def add_service(self, service):
        self._services.append(service)

    def update_mileage(self, new_mileage):
        if new_mileage < self._mileage:
            raise ValueError(
                f"New mileage ({new_mileage}) cannot be less than current mileage ({self._mileage})."
            )
        self._mileage = new_mileage

    def details(self):
        services = ", ".join(self._services) if self._services else "None"
        return (
            f"ID:       {self._id}\n"
            f"Make:     {self._make}\n"
            f"Model:    {self._model}\n"
            f"Year:     {self._year}\n"
            f"Mileage:  {self._mileage}\n"
            f"Services: {services}"
        )

    def __str__(self):
        return f"[{self._id}] {self._year} {self._make} {self._model} - {self._mileage} miles"


# ---------------- Input helpers ----------------

def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def ask_int(prompt, minimum=0):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if number < minimum:
            print(f"Please enter a number of at least {minimum}.")
            continue
        return number


def ask_for_car():
    if Car.get_total_cars() == 0:
        print("There are no cars yet. Add one first.")
        return None
    car = Car.find_car(ask_int("Enter the car ID: ", minimum=1))
    if car is None:
        print("No car found with that ID.")
    return car


# ---------------- Menu actions ----------------

def add_car():
    make = ask_text("Make: ")
    model = ask_text("Model: ")
    year = ask_int("Year: ", minimum=1886)  # first automobile
    mileage = ask_int("Mileage: ")
    car = Car(make, model, year, mileage)
    print(f"Added car: {car}")


def view_all_cars():
    cars = Car.get_all_cars()
    if not cars:
        print("There are no cars yet.")
        return
    for car in cars:
        print(car)


def view_total_cars():
    print(f"Total number of cars: {Car.get_total_cars()}")


def see_car_details():
    car = ask_for_car()
    if car:
        print(car.details())


def service_car():
    car = ask_for_car()
    if car:
        service = ask_text("Describe the service performed: ")
        car.add_service(service)
        print(f"Service added to car {car.id}.")


def update_mileage():
    car = ask_for_car()
    if car:
        new_mileage = ask_int("New mileage: ")
        try:
            car.update_mileage(new_mileage)
            print(f"Mileage updated: {car}")
        except ValueError as error:
            print(error)


MENU = """
----  WELCOME  ----
1. Add a car
2. View all cars
3. View total number of cars
4. See a car's details
5. Service a car
6. Update mileage
7. Quit"""

ACTIONS = {
    "1": add_car,
    "2": view_all_cars,
    "3": view_total_cars,
    "4": see_car_details,
    "5": service_car,
    "6": update_mileage,
}


def main():
    while True:
        print(MENU)
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            print()
            action()
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
