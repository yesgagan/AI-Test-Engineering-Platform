import ast
import subprocess
import sys
import tempfile
import os


def create_mutants(code):
    mutants = []

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return mutants

    for node in ast.walk(tree):

        # Mutation: change + to -
        if isinstance(node, ast.Add):
            mutant_tree = ast.fix_missing_locations(
                ReplaceOperator(ast.Add, ast.Sub).visit(
                    ast.parse(code)
                )
            )

            mutants.append({
                "type": "ADD_TO_SUBTRACT",
                "code": ast.unparse(mutant_tree)
            })

            break

    return mutants


class ReplaceOperator(ast.NodeTransformer):

    def __init__(self, old_operator, new_operator):
        self.old_operator = old_operator
        self.new_operator = new_operator

    def visit_BinOp(self, node):
        self.generic_visit(node)

        if isinstance(node.op, self.old_operator):
            node.op = self.new_operator()

        return node


def run_mutation_test(original_code, test_code):
    """
    Creates mutants and runs the tests against each mutant.
    """

    mutants = create_mutants(original_code)

    results = []

    if not mutants:
        return results

    for mutant in mutants:

        with tempfile.TemporaryDirectory() as temp_dir:

            code_file = os.path.join(
                temp_dir,
                "user_code.py"
            )

            test_file = os.path.join(
                temp_dir,
                "test_user_code.py"
            )

            # Save mutated code
            with open(
                code_file,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(mutant["code"])

            # Save tests
            with open(
                test_file,
                "w",
                encoding="utf-8"
            ) as file:
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

                # Tests failed = mutant was detected
                if result.returncode != 0:
                    status = "KILLED"

                # Tests passed = mutant survived
                else:
                    status = "SURVIVED"

                results.append({
                    "type": mutant["type"],
                    "status": status,
                    "mutant_code": mutant["code"],
                    "output": result.stdout,
                    "errors": result.stderr
                })

            except subprocess.TimeoutExpired:

                results.append({
                    "type": mutant["type"],
                    "status": "TIMEOUT",
                    "mutant_code": mutant["code"],
                    "output": "",
                    "errors": "Mutation test timed out."
                })

            except Exception as error:

                results.append({
                    "type": mutant["type"],
                    "status": "ERROR",
                    "mutant_code": mutant["code"],
                    "output": "",
                    "errors": str(error)
                })

    return results


def calculate_mutation_score(results):
    """
    Calculates mutation score.

    Mutation Score =
    Killed Mutants / Total Mutants * 100
    """

    if not results:
        return 0

    killed = sum(
        1
        for result in results
        if result["status"] == "KILLED"
    )

    total = len(results)

    score = (killed / total) * 100

    return round(score, 2)