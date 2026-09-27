import ast


def analyze_code(code):
    result = {
        "functions": [],
        "lines": len(code.splitlines()),
        "issues": [],
        "suggestions": []
    }

    # Check whether code is valid Python
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        result["issues"].append(
            f"Syntax error at line {error.lineno}"
        )
        return result

    # Find functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            result["functions"].append(node.name)

    # Generate basic test suggestions
    for function in result["functions"]:
        result["suggestions"].append(
            f"Test normal input for '{function}'"
        )

        result["suggestions"].append(
            f"Test boundary values for '{function}'"
        )

        result["suggestions"].append(
            f"Test invalid input for '{function}'"
        )

    # Detect division operation
    if "/" in code:
        result["suggestions"].append(
            "Test division by zero"
        )

    # If no functions are found
    if not result["functions"]:
        result["issues"].append(
            "No Python functions detected."
        )

    return result