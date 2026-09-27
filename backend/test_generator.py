def generate_tests(code):
    tests = []

    if "def add" in code:
        tests.append("""
def test_add_normal():
    from user_code import add
    assert add(2, 3) == 5
""")

    if "def subtract" in code:
        tests.append("""
def test_subtract_normal():
    from user_code import subtract
    assert subtract(5, 3) == 2
""")

    if "def multiply" in code:
        tests.append("""
def test_multiply_normal():
    from user_code import multiply
    assert multiply(4, 3) == 12
""")

    if "def divide" in code:
        tests.append("""
def test_divide_normal():
    from user_code import divide
    assert divide(10, 2) == 5
""")

        tests.append("""
def test_divide_by_zero():
    from user_code import divide
    assert divide(10, 0) is None
""")

    return "\n".join(tests)