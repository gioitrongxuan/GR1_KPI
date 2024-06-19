# Test Case 1: Empty Solution
sol = []
print(anneal(sol))
# Expected Output: ([], 0)

# Test Case 2: Solution with one element
sol = [5]
print(anneal(sol))
# Expected Output: ([5], cost(5))

# Test Case 3: Solution with multiple elements
sol = [2, 4, 6, 8, 10]
print(anneal(sol))
# Expected Output: ([optimized_solution], optimized_cost)

# Test Case 4: Solution with negative elements
sol = [-3, -1, 0, 2, 4]
print(anneal(sol))
# Expected Output: ([optimized_solution], optimized_cost)

# Test Case 5: Solution with duplicate elements
sol = [1, 2, 3, 3, 2, 1]
print(anneal(sol))
# Expected Output: ([optimized_solution], optimized_cost)