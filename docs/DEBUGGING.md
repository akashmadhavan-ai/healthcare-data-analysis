# Healthcare Data Analysis — Debugging Guide

# 1. Introduction

This document contains debugging procedures, troubleshooting workflows, and common issue resolutions for the Healthcare Data Analysis project.

The goal of this guide is to help developers:

- Identify common issues
- Understand root causes
- Fix environment problems
- Resolve import errors
- Debug analytics workflows
- Troubleshoot Git issues
- Recover broken virtual environments

This guide focuses on practical debugging rather than theoretical explanations.

---

# 2. Debugging Philosophy

The project follows a layered debugging approach.

```plaintext
Environment
    ↓
Dependencies
    ↓
Imports
    ↓
Execution
    ↓
Analytics Logic
    ↓
Visualization
```

Most beginner debugging mistakes happen because developers skip layers.

Example:

```plaintext
Import error
```

is usually:
- virtual environment issue
- wrong interpreter
- missing package

NOT:
```plaintext
bad code
```

---

# 3. Virtual Environment Issues

---

# 3.1 Problem — Virtual Environment Not Activated

## Symptoms

```plaintext
ModuleNotFoundError
```

OR:

```plaintext
Import could not be resolved
```

---

## Root Cause

The project virtual environment is not active.

---

## Solution

### PowerShell

```powershell
.\venv\Scripts\activate
```

### Git Bash

```bash
source venv/Scripts/activate
```

---

## Verification

You should see:

```plaintext
(venv)
```

before the terminal path.

Example:

```plaintext
(venv) Akash@LAPTOP...
```

---

# 3.2 Problem — Wrong Python Interpreter

## Symptoms

- Pylance import errors
- Packages installed but unresolved
- VS Code cannot detect modules

---

## Root Cause

VS Code is using the wrong Python interpreter.

---

## Solution

Open Command Palette:

```plaintext
Ctrl + Shift + P
```

Search:

```plaintext
Python: Select Interpreter
```

Select:

```plaintext
./venv/Scripts/python.exe
```

---

## Verification

Run:

```bash
where python
```

Expected:

```plaintext
.../healthcare-data-analysis/venv/Scripts/python.exe
```

---

# 3.3 Problem — Broken Virtual Environment

## Symptoms

- Dependency conflicts
- Random import failures
- Package corruption

---

## Solution

---

### Step 1 — Delete venv

PowerShell:

```powershell
Remove-Item -Recurse -Force venv
```

Git Bash:

```bash
rm -rf venv
```

---

### Step 2 — Recreate venv

```bash
python -m venv venv
```

---

### Step 3 — Activate

```bash
source venv/Scripts/activate
```

---

### Step 4 — Reinstall Dependencies

```bash
python -m pip install -r requirements.txt
```

---

# 4. Dependency Issues

---

# 4.1 Problem — reportlab Import Error

## Error

```plaintext
Import "reportlab" could not be resolved
```

---

## Root Cause

reportlab package is not installed inside the active virtual environment.

---

## Solution

```bash
python -m pip install reportlab
```

---

## Verification

```bash
python -m pip show reportlab
```

Expected location:

```plaintext
.../venv/Lib/site-packages
```

NOT:

```plaintext
AppData/Roaming/Python
```

---

# 4.2 Problem — plotly Import Error

## Error

```plaintext
ModuleNotFoundError: plotly
```

---

## Solution

```bash
python -m pip install plotly
```

---

# 4.3 Problem — pandas Import Error

## Solution

```bash
python -m pip install pandas
```

---

# 4.4 Problem — Missing Multiple Dependencies

## Solution

```bash
python -m pip install -r requirements.txt
```

---

# 4.5 Problem — pip Installing to Wrong Python

## Symptoms

- Package installed
- Still unresolved imports

---

## Root Cause

Using:

```bash
pip install package
```

instead of:

```bash
python -m pip install package
```

---

## Correct Approach

Always use:

```bash
python -m pip install package-name
```

---

# 5. Import Issues

---

# 5.1 Problem — ModuleNotFoundError

## Error Example

```plaintext
ModuleNotFoundError: No module named 'core'
```

---

## Root Cause

Running files directly instead of as Python modules.

---

## Wrong

```bash
python tests/test_loader.py
```

---

## Correct

```bash
python -m tests.test_loader
```

---

# 5.2 Problem — Relative Import Failure

## Root Cause

Incorrect project execution path.

---

## Solution

Always execute commands from:

```plaintext
healthcare-data-analysis/
```

NOT:

```plaintext
tests/
```

---

# 6. Git Issues

---

# 6.1 Problem — No Upstream Branch

## Error

```plaintext
fatal: The current branch has no upstream branch
```

---

## Solution

```bash
git push -u origin branch-name
```

---

# 6.2 Problem — Changes Not Appearing on GitHub

## Root Cause

Changes committed locally but not pushed.

---

## Solution

```bash
git push
```

---

# 6.3 Problem — Main Branch Not Updated

## Root Cause

Changes merged into dev but not merged into main.

---

## Solution

```bash
git checkout main
git merge dev
git push origin main
```

---

# 6.4 Problem — Merge Conflicts

## Symptoms

```plaintext
CONFLICT (content)
```

---

## Solution Workflow

1. Open conflicted file
2. Remove conflict markers

Example:

```plaintext
<<<<<<< HEAD
=======
>>>>>>> branch-name
```

3. Keep correct code
4. Save file
5. Commit merge

---

# 7. Dataset Issues

---

# 7.1 Problem — Dataset Not Found

## Error

```plaintext
Dataset 'diabetes' not found
```

---

## Root Cause

Dataset missing from:

```plaintext
sample_data/
```

---

## Solution

Verify:

```plaintext
sample_data/diabetes.csv
```

exists.

---

# 7.2 Problem — Empty DataFrame

## Root Cause

Incorrect CSV loading.

---

## Debugging

```python
print(df.shape)
print(df.head())
```

---

# 7.3 Problem — CSV Parsing Errors

## Solution

Try:

```python
pd.read_csv(
    "file.csv",
    encoding="utf-8"
)
```

OR:

```python
pd.read_csv(
    "file.csv",
    encoding="latin1"
)
```

---

# 8. Analytics Issues

---

# 8.1 Problem — Correlation Matrix Empty

## Root Cause

Dataset has insufficient numeric columns.

---

## Verification

```python
print(analyzer.numeric_cols)
```

---

# 8.2 Problem — Outlier Detection Fails

## Root Cause

Non-numeric columns passed to statistical methods.

---

## Solution

Verify column datatype.

```python
print(df.dtypes)
```

---

# 8.3 Problem — Quality Score Incorrect

## Root Cause

Dataset contains unexpected missing values or duplicates.

---

## Verification

```python
print(df.isna().sum())
print(df.duplicated().sum())
```

---

# 9. Visualization Issues

---

# 9.1 Problem — Blank Charts

## Root Cause

Invalid columns passed into visualizer.

---

## Solution

Verify columns exist.

```python
print(df.columns)
```

---

# 9.2 Problem — Plotly Not Rendering

## Solution

Install Plotly.

```bash
python -m pip install plotly
```

---

# 9.3 Problem — Heatmap Generation Failure

## Root Cause

Insufficient numeric columns.

---

## Solution

Verify numeric column count.

```python
print(len(visualizer.numeric_cols))
```

---

# 10. Report Generation Issues

---

# 10.1 Problem — PDF Not Generated

## Root Cause

reportlab missing.

---

## Solution

```bash
python -m pip install reportlab
```

---

# 10.2 Problem — Permission Denied on PDF Export

## Root Cause

PDF currently open during overwrite.

---

## Solution

Close existing PDF before regeneration.

---

# 11. Testing Issues

---

# 11.1 Problem — Tests Not Running

## Root Cause

Wrong execution command.

---

## Correct

```bash
python -m tests.test_loader
```

---

# 11.2 Problem — Assertion Failures

## Root Cause

Unexpected dataset structure.

---

## Debugging

Print:

```python
print(df.columns)
print(df.head())
```

---

# 12. VS Code Issues

---

# 12.1 Problem — Pylance Warnings Persist

## Solution

Reload VS Code window.

Open Command Palette:

```plaintext
Ctrl + Shift + P
```

Search:

```plaintext
Developer: Reload Window
```

---

# 12.2 Problem — IntelliSense Missing

## Root Cause

Python extension missing.

---

## Solution

Install:
- Python Extension
- Pylance

---

# 13. Streamlit Issues (Future)

---

# 13.1 Problem — Streamlit Command Not Found

## Solution

```bash
python -m pip install streamlit
```

---

# 13.2 Problem — Port Already in Use

## Solution

Run on another port.

```bash
streamlit run app.py --server.port 8502
```

---

# 14. Debugging Workflow

The recommended debugging order:

```plaintext
1. Verify venv
        ↓
2. Verify interpreter
        ↓
3. Verify dependencies
        ↓
4. Verify imports
        ↓
5. Verify dataset
        ↓
6. Verify execution command
        ↓
7. Debug analytics logic
```

Most issues are solved in steps 1–3.

---

# 15. Logging Recommendations

Useful debugging prints:

```python
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.head())
```

---

# 16. Best Practices

---

## Always Activate venv

Before development.

---

## Always Use python -m pip

Avoid interpreter mismatch issues.

---

## Always Run Tests Before Push

Example:

```bash
python -m tests.test_loader
```

---

## Always Verify Branch Before Commit

```bash
git branch
```

---

## Always Push After Commit

```bash
git push
```

---

# 17. Recovery Strategy

If the project becomes unstable:

```plaintext
Delete venv
        ↓
Recreate venv
        ↓
Install requirements
        ↓
Verify interpreter
        ↓
Run tests
```

This resolves most environment-related failures.

---

# 18. Future Debugging Expansion

Future versions may include debugging support for:

- Streamlit dashboards
- ML pipelines
- Cloud deployment
- Docker
- REST APIs

---

# 19. Conclusion

This debugging guide provides structured troubleshooting procedures for:

- Environment issues
- Dependency issues
- Git issues
- Analytics issues
- Visualization issues
- Reporting issues

The goal is to simplify debugging and improve developer productivity across the Healthcare Data Analysis platform.