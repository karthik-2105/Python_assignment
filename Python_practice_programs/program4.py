# Generate a list of numbers from 1 to 20
numbers = list(range(1, 21))

# Use map() with lambda to calculate squares
squares = list(map(lambda x: x ** 2, numbers))

print(squares)
