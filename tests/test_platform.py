import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "backend"
        )
    )
)

from analyzer import analyze_code
from test_generator import generate_tests
from mutation import run_mutation_test, calculate_mutation_score
from flaky_detector import detect_flaky_tests


def test_valid_code_analysis():

    code = """
def add(a, b):
    return a + b
"""

    result = analyze_code(code)

    assert "add" in result["functions"]
    assert len(result["issues"]) == 0


def test_invalid_code_detection():

    code = """
def add(a, b)
    return a + b
"""

    result = analyze_code(code)

    assert len(result["issues"]) > 0
    assert "Syntax error" in result["issues"][0]


def test_test_generation():

    code = """
def add(a, b):
    return a + b
"""

    tests = generate_tests(code)

    assert "test_add_normal" in tests


def test_mutation_testing():

    code = """
def add(a, b):
    return a + b
"""

    tests = """
from user_code import add

def test_add():
    assert add(2, 3) == 5
"""

    results = run_mutation_test(
        code,
        tests
    )

    score = calculate_mutation_score(
        results
    )

    assert len(results) == 1
    assert results[0]["status"] == "KILLED"
    assert score == 100.0


def test_flaky_detector():

    code = """
def add(a, b):
    return a + b
"""

    tests = """
from user_code import add

def test_add():
    assert add(2, 3) == 5
"""

    result = detect_flaky_tests(
        code,
        tests,
        runs=3
    )

    assert result["runs"] == 3
    assert result["passed"] == 3
    assert result["failed"] == 0
    assert result["is_flaky"] is False