from itertools import product

def generate_combinations(*lists):
    # Generate all combinations using product, which computes the Cartesian product
    combinations = product(*lists)
    # Convert each combination (which is a tuple) to a list
    return [list(combination) for combination in combinations]

# Example usage:
list1 = [1, 2]
list2 = [3, 4]
list3 = [5, 6]
result = generate_combinations(list1, list2, list3)
print(result)
