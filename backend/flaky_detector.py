import subprocess
import sys
import tempfile
import os


def detect_flaky_tests(code, test_code, runs=5):
    """
    Runs the same test suite multiple times
    and checks for inconsistent results.
    """

    results = []

    with tempfile.TemporaryDirectory() as temp_dir:

        code_file = os.path.join(
            temp_dir,
            "user_code.py"
        )

        test_file = os.path.join(
            temp_dir,
            "test_user_code.py"
        )

        # Save user code
        with open(
            code_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(code)

        # Save tests
        with open(
            test_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(test_code)

        # Run tests multiple times
        for run in range(runs):

            try:

                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pytest",
                        test_file,
                        "-q"
                    ],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=20
                )

                if result.returncode == 0:
                    status = "PASSED"
                else:
                    status = "FAILED"

                results.append(status)

            except subprocess.TimeoutExpired:

                results.append("TIMEOUT")

            except Exception:

                results.append("ERROR")


    # Count passed and failed runs
    passed = results.count("PASSED")
    failed = results.count("FAILED")

    # A test suite is considered flaky
    # if it has both pass and fail results.
    is_flaky = passed > 0 and failed > 0

    return {
        "runs": runs,
        "results": results,
        "passed": passed,
        "failed": failed,
        "is_flaky": is_flaky
    }