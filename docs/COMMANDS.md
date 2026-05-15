# Healthcare Data Analysis — Developer Commands Guide

# 1. Introduction

This document contains all commonly used commands for developing, testing, debugging, and managing the Healthcare Data Analysis project.

The goal of this file is to provide a centralized developer command reference for:

- Environment setup
- Dependency management
- Testing
- Git workflow
- Streamlit execution
- Debugging
- Branch management

This file acts as a quick-access developer cheat sheet.

---

# 2. Project Navigation Commands

---

## 2.1 Open Project Folder

```bash
cd healthcare-data-analysis
```

---

## 2.2 Verify Current Directory

### Windows

```bash
pwd
```

---

# 3. Virtual Environment Commands

The project uses a Python virtual environment for dependency isolation.

---

# 3.1 Create Virtual Environment

```bash
python -m venv venv
```

---

# 3.2 Activate Virtual Environment

---

## PowerShell

```powershell
.\venv\Scripts\activate
```

---

## Git Bash

```bash
source venv/Scripts/activate
```

---

# 3.3 Deactivate Virtual Environment

```bash
deactivate
```

---

# 3.4 Verify Active Python Interpreter

```bash
where python
```

Expected output:

```plaintext
.../healthcare-data-analysis/venv/Scripts/python.exe
```

---

# 4. Python Package Commands

---

# 4.1 Install All Dependencies

```bash
python -m pip install -r requirements.txt
```

---

# 4.2 Install Single Package

```bash
python -m pip install pandas
```

Example:

```bash
python -m pip install reportlab
```

---

# 4.3 Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 4.4 View Installed Packages

```bash
pip list
```

---

# 4.5 Verify Package Installation

```bash
python -m pip show pandas
```

---

# 4.6 Update requirements.txt

```bash
pip freeze > requirements.txt
```

---

# 4.7 Remove Package

```bash
python -m pip uninstall package-name
```

---

# 5. VS Code Commands

---

# 5.1 Open VS Code

```bash
code .
```

---

# 5.2 Open Command Palette

```plaintext
Ctrl + Shift + P
```

---

# 5.3 Select Python Interpreter

Search:

```plaintext
Python: Select Interpreter
```

Select:

```plaintext
./venv/Scripts/python.exe
```

---

# 5.4 Reload VS Code Window

Search:

```plaintext
Developer: Reload Window
```

---

# 6. Dataset Commands

---

# 6.1 Verify Dataset Folder

```bash
dir sample_data
```

Git Bash:

```bash
ls sample_data
```

---

# 6.2 Open CSV Dataset

```bash
python
```

```python
import pandas as pd

df = pd.read_csv(
    "sample_data/diabetes.csv"
)

print(df.head())
```

---

# 7. Test Execution Commands

---

# 7.1 Run Loader Tests

```bash
python -m tests.test_loader
```

---

# 7.2 Run Cleaner Tests

```bash
python -m tests.test_cleaner
```

---

# 7.3 Run Analyzer Tests

```bash
python -m tests.test_analyzer
```

---

# 7.4 Run Insight Tests

```bash
python -m tests.test_insights
```

---

# 7.5 Run Visualizer Tests

```bash
python -m tests.test_visualizer
```

---

# 7.6 Run Report Tests

```bash
python -m tests.test_report
```

---

# 7.7 Run Pipeline Tests

```bash
python -m tests.test_pipeline
```

---

# 8. Streamlit Commands

Future dashboard system commands.

---

# 8.1 Run Streamlit App

```bash
streamlit run app.py
```

---

# 8.2 Run Streamlit on Custom Port

```bash
streamlit run app.py --server.port 8502
```

---

# 8.3 Stop Streamlit

```plaintext
CTRL + C
```

---

# 9. Git Commands

---

# 9.1 Verify Git Status

```bash
git status
```

---

# 9.2 View Branches

```bash
git branch
```

---

# 9.3 View Remote Branches

```bash
git branch -r
```

---

# 9.4 Create Feature Branch

```bash
git checkout -b feature/analytics-core
```

---

# 9.5 Switch Branch

```bash
git checkout dev
```

Example:

```bash
git checkout staging
```

---

# 9.6 Stage Files

```bash
git add .
```

---

# 9.7 Commit Changes

```bash
git commit -m "feat: implement analytics core infrastructure"
```

---

# 9.8 Push Feature Branch

```bash
git push -u origin feature/analytics-core
```

---

# 9.9 Push Current Branch

```bash
git push
```

---

# 9.10 Pull Latest Changes

```bash
git pull origin dev
```

---

# 9.11 Merge Branches

Example:

```bash
git checkout dev
git merge feature/analytics-core
```

---

# 9.12 Delete Local Branch

```bash
git branch -d feature/analytics-core
```

---

# 9.13 Delete Remote Branch

```bash
git push origin --delete feature/analytics-core
```

---

# 9.14 View Commit History

```bash
git log --oneline
```

---

# 9.15 View Detailed Branch Tracking

```bash
git branch -vv
```

---

# 10. Output Folder Commands

---

# 10.1 View Generated Reports

```bash
dir outputs/reports
```

Git Bash:

```bash
ls outputs/reports
```

---

# 10.2 Delete Generated Outputs

PowerShell:

```powershell
Remove-Item outputs/reports/*
```

Git Bash:

```bash
rm -rf outputs/reports/*
```

---

# 11. Debugging Commands

---

# 11.1 Verify Python Version

```bash
python --version
```

---

# 11.2 Verify pip Version

```bash
pip --version
```

---

# 11.3 Verify Active Environment Packages

```bash
pip list
```

---

# 11.4 Test reportlab Installation

```bash
python -m pip show reportlab
```

---

# 11.5 Verify Plotly Installation

```bash
python -m pip show plotly
```

---

# 11.6 Verify Streamlit Installation

```bash
python -m pip show streamlit
```

---

# 12. File Structure Commands

---

# 12.1 View Complete Folder Structure

PowerShell:

```powershell
tree /f
```

Git Bash:

```bash
find .
```

---

# 12.2 Create New Python File

PowerShell:

```powershell
New-Item test.py
```

Git Bash:

```bash
touch test.py
```

---

# 12.3 Create New Folder

```bash
mkdir folder_name
```

---

# 13. Common Recovery Commands

---

# 13.1 Reinstall All Dependencies

```bash
python -m pip install -r requirements.txt --force-reinstall
```

---

# 13.2 Remove Virtual Environment

PowerShell:

```powershell
Remove-Item -Recurse -Force venv
```

Git Bash:

```bash
rm -rf venv
```

---

# 13.3 Recreate Virtual Environment

```bash
python -m venv venv
```

Activate again afterward.

---

# 14. Dependency Troubleshooting Commands

---

# 14.1 Fix reportlab Issues

```bash
python -m pip install reportlab
```

---

# 14.2 Fix Plotly Issues

```bash
python -m pip install plotly
```

---

# 14.3 Fix Missing Packages

```bash
python -m pip install -r requirements.txt
```

---

# 15. Recommended Development Workflow

```plaintext
Create Feature Branch
        ↓
Write Code
        ↓
Run Tests
        ↓
Commit Changes
        ↓
Push Feature Branch
        ↓
Merge into Dev
        ↓
Merge into Staging
        ↓
Merge into Main
```

---

# 16. Recommended Commit Prefixes

| Prefix | Purpose |
|--------|----------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| refactor | Code restructuring |
| test | Testing |
| release | Production release |

---

# 17. Example Full Workflow

---

## Step 1 — Create Feature Branch

```bash
git checkout -b feature/dashboard-system
```

---

## Step 2 — Add Files

```bash
git add .
```

---

## Step 3 — Commit

```bash
git commit -m "feat: implement dashboard visualization system"
```

---

## Step 4 — Push Branch

```bash
git push -u origin feature/dashboard-system
```

---

## Step 5 — Merge to Dev

```bash
git checkout dev
git merge feature/dashboard-system
```

---

# 18. Best Practices

---

## Always Activate venv

Before development:

```bash
source venv/Scripts/activate
```

---

## Always Use python -m pip

Correct:

```bash
python -m pip install pandas
```

Wrong:

```bash
pip install pandas
```

Reason:
- Prevents interpreter mismatch issues.

---

## Always Run Tests Before Push

```bash
python -m tests.test_loader
```

---

## Always Update requirements.txt

```bash
pip freeze > requirements.txt
```

---

# 19. Future Commands

Upcoming features may include commands for:

- Docker
- CI/CD
- Cloud deployment
- REST APIs
- ML pipelines

---

# 20. Conclusion

This document serves as the centralized command reference for the Healthcare Data Analysis project.

The commands support:

- Development
- Debugging
- Dependency management
- Git workflow
- Analytics testing
- Environment setup

Using standardized commands improves:
- development consistency
- debugging speed
- onboarding experience
- project maintainability