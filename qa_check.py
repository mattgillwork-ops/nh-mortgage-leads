# Anti-Gravity Quality Assurance Protocol
# ========================================
# Runs automated checks on all agent-generated code BEFORE it is committed.
# This prevents the types of bugs found in the Cloud Audit from recurring.
#
# Usage: py qa_check.py [file_or_directory]

import os
import sys
import re
import ast
import importlib


def check_error_handling(filepath: str) -> list:
    """Checks that all requests.get() calls have try/except and timeout."""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all requests.get() calls
    get_calls = [(i+1, line) for i, line in enumerate(content.split('\n')) if 'requests.get(' in line]
    
    for line_num, line in get_calls:
        if 'timeout' not in line:
            issues.append(f"  [{filepath}:{line_num}] requests.get() missing timeout parameter")
    
    # Check if requests.get is used but no try/except exists in the function
    if 'requests.get(' in content and 'except' not in content:
        issues.append(f"  [{filepath}] Uses requests.get() but has no try/except error handling")
    
    return issues


def check_path_security(filepath: str) -> list:
    """Checks that all path boundary checks are case-insensitive on Windows."""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if '.startswith(' in line and ('base_dir' in line or 'workspace' in line.lower()):
            if '.lower()' not in line:
                issues.append(f"  [{filepath}:{i+1}] Path boundary check is NOT case-insensitive (missing .lower())")
    
    return issues


def check_text_truncation(filepath: str) -> list:
    """Checks that agent tools truncate text output to prevent context overflow."""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'get_text(' in content:
        # Check if there's any truncation ([:N] or max_chars or similar)
        if '[:' not in content and 'max_chars' not in content and 'truncat' not in content.lower():
            issues.append(f"  [{filepath}] Uses get_text() but never truncates the output — risk of context overflow")
    
    return issues


def check_syntax(filepath: str) -> list:
    """Checks that a Python file has valid syntax."""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
    except SyntaxError as e:
        issues.append(f"  [{filepath}:{e.lineno}] Syntax Error: {e.msg}")
    return issues


def check_hardcoded_strings(filepath: str) -> list:
    """Checks for hardcoded agent names in prompts that should be dynamic."""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        # Look for input() calls with hardcoded agent names
        if 'input(' in line and ('for the Coder' in line or 'for the Marketing' in line or 'for the DevOps' in line):
            if '{' not in line:  # Not an f-string
                issues.append(f"  [{filepath}:{i+1}] Hardcoded agent name in user prompt — should use f-string with variable")
    
    return issues


def check_deprecated_imports(filepath: str) -> list:
    """Checks for deprecated package imports."""
    issues = []
    deprecated = {
        'google.generativeai': 'Migrate to google-genai SDK',
    }
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pkg, fix in deprecated.items():
        if f'import {pkg}' in content:
            issues.append(f"  [{filepath}] Uses deprecated package '{pkg}'. {fix}")
    
    return issues


def check_playwright_content(filepath: str) -> list:
    """Checks for the use of page.content() which returns raw HTML instead of visible text."""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'playwright' in content and '.content()' in content:
        issues.append(f"  [{filepath}] Uses page.content() with Playwright. This returns raw HTML. Use page.text_content('body') instead for visible text.")
    
    return issues


def run_qa(target_path: str):
    """Run all QA checks on a file or directory."""
    
    print("=" * 56)
    print("  [QA] Anti-Gravity Quality Assurance Check")
    print("=" * 56)
    
    # Collect all .py files
    py_files = []
    if os.path.isfile(target_path):
        py_files = [target_path]
    else:
        for root, dirs, files in os.walk(target_path):
            # Skip __pycache__ and .git
            dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git')]
            for f in files:
                if f.endswith('.py') and f not in ('qa_check.py', 'agent_router.py'):
                    py_files.append(os.path.join(root, f))
    
    all_issues = []
    checks = [
        ("Syntax Validation", check_syntax),
        ("Error Handling", check_error_handling),
        ("Path Security", check_path_security),
        ("Text Truncation", check_text_truncation),
        ("Hardcoded Strings", check_hardcoded_strings),
        ("Deprecated Imports", check_deprecated_imports),
        ("Playwright Content", check_playwright_content),
    ]
    
    for check_name, check_fn in checks:
        print(f"\n  Running: {check_name}...")
        check_issues = []
        for filepath in py_files:
            check_issues.extend(check_fn(filepath))
        
        if check_issues:
            print(f"  ISSUES FOUND ({len(check_issues)}):")
            for issue in check_issues:
                print(f"    {issue}")
            all_issues.extend(check_issues)
        else:
            print(f"  PASS")
    
    print("\n" + "=" * 56)
    if all_issues:
        print(f"  RESULT: {len(all_issues)} issue(s) found. Review required.")
    else:
        print(f"  RESULT: ALL CHECKS PASSED")
    print("=" * 56)
    
    return len(all_issues) == 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    success = run_qa(target)
    sys.exit(0 if success else 1)
