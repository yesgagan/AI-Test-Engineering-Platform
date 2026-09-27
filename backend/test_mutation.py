from mutation import run_mutation_test, calculate_mutation_score


code = """
def add(a, b):
    return a + b
"""


tests = """
from user_code import add


def test_add():
    assert add(2, 3) == 5
"""


results = run_mutation_test(code, tests)

print("Mutation Results:")
print(results)

print("Mutation Score:", calculate_mutation_score(results))