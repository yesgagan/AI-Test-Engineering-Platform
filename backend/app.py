
from flask import Flask, render_template, request, jsonify

from analyzer import analyze_code
from test_generator import generate_tests
from test_runner import run_tests
from mutation import run_mutation_test, calculate_mutation_score
from flaky_detector import detect_flaky_tests
from baseline import run_baseline


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    code = data.get("code", "")
    requirement = data.get("requirement", "")

    # ---------------------------------------------------------
    # STEP 1: ANALYZE SOURCE CODE
    # ---------------------------------------------------------

    result = analyze_code(code)

    # ---------------------------------------------------------
    # STEP 2: STOP TEST GENERATION IF CODE HAS SYNTAX ERROR
    # ---------------------------------------------------------

    has_syntax_error = len(result.get("issues", [])) > 0

    if has_syntax_error:

        result["requirement"] = requirement

        result["generated_tests"] = ""

        result["test_execution"] = {
            "success": False,
            "output": "",
            "errors": "Test generation skipped because the source code contains a syntax error."
        }

        result["baseline"] = {
            "method": "Simple baseline testing",
            "passed": False,
            "output": "",
            "errors": "Baseline testing skipped because the source code contains a syntax error."
        }

        result["mutation_results"] = []

        result["mutation_score"] = 0

        result["flaky_results"] = {
            "runs": 0,
            "results": [],
            "passed": 0,
            "failed": 0,
            "is_flaky": False
        }

        result["suggestions"] = [
            "Fix the syntax error before generating test cases."
        ]

        return jsonify(result)

    # ---------------------------------------------------------
    # STEP 3: GENERATE TESTS
    # ---------------------------------------------------------

    test_code = generate_tests(code)

    # ---------------------------------------------------------
    # STEP 4: EXECUTE GENERATED TESTS
    # ---------------------------------------------------------

    if test_code.strip():

        execution = run_tests(
            code,
            test_code
        )

    else:

        execution = {
            "success": False,
            "output": "",
            "errors": "No suitable tests could be generated."
        }

    # ---------------------------------------------------------
    # STEP 5: BASELINE
    # ---------------------------------------------------------

    baseline_result = {
        "method": "Simple baseline testing",
        "passed": False,
        "output": "",
        "errors": "No suitable tests were generated."
    }

    if test_code.strip():

        baseline_result = run_baseline(
            code,
            test_code
        )

    # ---------------------------------------------------------
    # STEP 6: MUTATION TESTING
    # ---------------------------------------------------------

    mutation_results = []

    mutation_score = 0

    if test_code.strip():

        mutation_results = run_mutation_test(
            code,
            test_code
        )

        mutation_score = calculate_mutation_score(
            mutation_results
        )

    # ---------------------------------------------------------
    # STEP 7: FLAKY TEST DETECTION
    # ---------------------------------------------------------

    flaky_results = {
        "runs": 0,
        "results": [],
        "passed": 0,
        "failed": 0,
        "is_flaky": False
    }

    if test_code.strip():

        flaky_results = detect_flaky_tests(
            code,
            test_code,
            runs=5
        )

    # ---------------------------------------------------------
    # STEP 8: FINAL RESPONSE
    # ---------------------------------------------------------

    result["requirement"] = requirement

    result["generated_tests"] = test_code

    result["test_execution"] = execution

    result["baseline"] = baseline_result

    result["mutation_results"] = mutation_results

    result["mutation_score"] = mutation_score

    result["flaky_results"] = flaky_results

    return jsonify(result)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

