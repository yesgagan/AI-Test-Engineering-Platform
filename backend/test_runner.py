import subprocess
import sys
import tempfile
import os


def run_tests(code, test_code):
    """
    Runs the submitted Python code with generated tests.
    Returns test execution results.
    """

    with tempfile.TemporaryDirectory() as temp_dir:

        code_file = os.path.join(temp_dir, "user_code.py")
        test_file = os.path.join(temp_dir, "test_user_code.py")

        # Save user's code
        with open(code_file, "w", encoding="utf-8") as file:
            file.write(code)

        # Save generated tests
        with open(test_file, "w", encoding="utf-8") as file:
            file.write(test_code)

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    test_file,
                    "-v"
                ],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=20
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "output": "",
                "errors": "Test execution timed out."
            }

        except Exception as error:

            return {
                "success": False,
                "output": "",
                "errors": str(error)
            }