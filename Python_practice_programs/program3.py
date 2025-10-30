# Given list
numbers = [12, 24, 35, 24, 88, 120, 155, 88, 120, 155]

# Create an empty list to store unique elements
unique_numbers = []
seen = set()

for num in numbers:
    if num not in seen:
        unique_numbers.append(num)
        seen.add(num)

print(unique_numbers)
