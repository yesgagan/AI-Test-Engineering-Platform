def run_baseline(code, test_code):
    """
    Simple baseline:
    Run the generated/basic tests once and record
    whether the test suite passes.

    This represents a simple testing process without
    mutation-based test-quality evaluation.
    """

    import subprocess
    import sys
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as temp_dir:

        code_file = os.path.join(temp_dir, "user_code.py")
        test_file = os.path.join(temp_dir, "test_user_code.py")

        with open(code_file, "w", encoding="utf-8") as file:
            file.write(code)

        with open(test_file, "w", encoding="utf-8") as file:
            file.write(test_code)

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

            return {
                "method": "Simple baseline testing",
                "passed": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "method": "Simple baseline testing",
                "passed": False,
                "output": "",
                "errors": "Baseline test execution timed out."
            }

        except Exception as error:
            return {
                "method": "Simple baseline testing",
                "passed": False,
                "output": "",
                "errors": str(error)
            }