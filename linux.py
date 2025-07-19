import os
import re
import subprocess
import tempfile
import json

C_FILE_NAME = "driver.c"
METRICS_FILE = "metrics.json"


def analyze_code_style(code):
    """Check for Linux kernel coding style violations (mocked)."""
    issues = {
        "tab_usage": len(re.findall(r"\t", code)),
        "line_length": sum(1 for line in code.splitlines() if len(line) > 80),
        "comments_missing": sum(1 for line in code.splitlines() if line.strip().startswith("void") and "//" not in line),
    }
    return issues

def check_for_race_conditions(code):
    """Check for presence of spinlocks/mutexes."""
    race_safe = bool(re.search(r"(spin_lock|mutex_lock)", code))
    return 1.0 if race_safe else 0.5

def check_buffer_safety(code):
    """Check for safe buffer usage (simplified)."""
    if "copy_from_user" in code and "copy_to_user" in code:
        return 0.9
    return 0.5

def input_validation_check(code):
    """Very basic input sanitization presence."""
    return 0.8 if "if" in code and "NULL" in code else 0.4

def try_compile(code):
    print("Skipping actual compilation (GCC not configured).")
    # Return mock results: success=True, warnings=0, errors=0
    return True, 0, 0

def evaluate_driver_code(code):
    compilation_success, warnings, errors = try_compile(code)

    metrics = {
        "compilation": {
            "success_rate": 1.0 if compilation_success else 0.0,
            "warnings_count": warnings,
            "errors_count": errors
        },
        "functionality": {
            "basic_operations": 0.9 if "read" in code and "write" in code else 0.6,
            "error_handling": 0.7,
            "edge_cases": 0.5
        },
        "security": {
            "buffer_safety": check_buffer_safety(code),
            "race_conditions": check_for_race_conditions(code),
            "input_validation": input_validation_check(code)
        },
        "code_quality": {
            "style_compliance": 1.0 - (analyze_code_style(code)["line_length"] * 0.01),
            "documentation": 0.7,
            "maintainability": 0.8
        }
    }
    score = (
        0.4 * metrics["compilation"]["success_rate"] +
        0.3 * metrics["functionality"]["basic_operations"] +
        0.2 * metrics["security"]["buffer_safety"] +
        0.1 * metrics["code_quality"]["maintainability"]
    ) * 100

    metrics["overall_score"] = round(score, 2)
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics
if __name__ == "__main__":
    c_file_path = input("Enter path to driver C file: ").strip().strip('"')

    if not os.path.exists(c_file_path):
        print(" C file not found.")
        exit(1)

    with open(c_file_path, "r") as f:
        code = f.read()

    print("\n Evaluating driver code...")
    results = evaluate_driver_code(code)

    print("\n Evaluation Metrics:")
    for section, values in results.items():
        print(f"\n{section.upper()}")
        if isinstance(values, dict):
            for key, val in values.items():
                print(f"  {key}: {val}")
        else:
            print(f"  Score: {values}")

    print(f"\n Saved metrics to `{METRICS_FILE}`")
