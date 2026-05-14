# 🔀 Healthcare Analytics Git Workflow

# 🌳 Branch Structure

```plaintext
main
↑
staging
↑
dev
↑
feature/*
```

---

# 📌 Branch Purpose

| Branch     | Purpose                         |
| ---------- | ------------------------------- |
| main       | Stable production-ready version |
| staging    | Pre-release testing branch      |
| dev        | Main development branch         |
| feature/\* | Individual feature development  |
| bugfix/\*  | Individual bug fixes            |

---

# 🚀 INITIAL SETUP

## Clone Repository

```bash
git clone https://github.com/akashmadhavan-ai/healthcare-data-analysis.git
```

---

## Move Into Repository

```bash
cd healthcare-data-analysis
```

---

# 🌿 CREATE MAIN BRANCHES

## Create Dev Branch

```bash
git checkout -b dev
```

```bash
git push -u origin dev
```

---

## Create Staging Branch

```bash
git checkout -b staging
```

```bash
git push -u origin staging
```

---

# ✨ FEATURE DEVELOPMENT WORKFLOW

# STEP 1 — SWITCH TO DEV

```bash
git checkout dev
```

---

# STEP 2 — PULL LATEST DEV

```bash
git pull origin dev
```

---

# STEP 3 — CREATE FEATURE BRANCH

Example:

```bash
git checkout -b feature/sample-loader
```

---

# STEP 4 — DEVELOP FEATURE

Make code changes.

---

# STEP 5 — CHECK STATUS

```bash
git status
```

---

# STEP 6 — ADD FILES

```bash
git add .
```

---

# STEP 7 — COMMIT CHANGES

Example:

```bash
git commit -m "feat: implement sample healthcare dataset loader"
```

---

# STEP 8 — PUSH FEATURE BRANCH

```bash
git push -u origin feature/sample-loader
```

---

# 🔁 MERGE FEATURE → DEV

# STEP 1 — SWITCH TO DEV

```bash
git checkout dev
```

---

# STEP 2 — MERGE FEATURE

```bash
git merge feature/sample-loader
```

---

# STEP 3 — PUSH DEV

```bash
git push origin dev
```

---

# 🧪 MERGE DEV → STAGING

# STEP 1 — SWITCH TO STAGING

```bash
git checkout staging
```

---

# STEP 2 — MERGE DEV

```bash
git merge dev
```

---

# STEP 3 — PUSH STAGING

```bash
git push origin staging
```

---

# 🚀 MERGE STAGING → MAIN

# STEP 1 — SWITCH TO MAIN

```bash
git checkout main
```

---

# STEP 2 — MERGE STAGING

```bash
git merge staging
```

---

# STEP 3 — PUSH MAIN

```bash
git push origin main
```

---

# 🐞 BUGFIX WORKFLOW

# STEP 1 — SWITCH TO DEV

```bash
git checkout dev
```

---

# STEP 2 — CREATE BUGFIX BRANCH

Example:

```bash
git checkout -b bugfix/chart-rendering
```

---

# STEP 3 — FIX ISSUE

Make required changes.

---

# STEP 4 — ADD FILES

```bash
git add .
```

---

# STEP 5 — COMMIT FIX

```bash
git commit -m "fix: resolve chart rendering issue"
```

---

# STEP 6 — PUSH BUGFIX

```bash
git push -u origin bugfix/chart-rendering
```

---

# STEP 7 — MERGE BUGFIX → DEV

```bash
git checkout dev
```

---

```bash
git merge bugfix/chart-rendering
```

---

```bash
git push origin dev
```

---

# 🔄 SYNC BRANCHES

## Update Dev From Main

```bash
git checkout dev
```

```bash
git merge main
```

```bash
git push origin dev
```

---

## Update Staging From Main

```bash
git checkout staging
```

```bash
git merge main
```

```bash
git push origin staging
```

---

# 📥 PULL LATEST CHANGES

## Pull Main

```bash
git checkout main
```

```bash
git pull origin main
```

---

## Pull Dev

```bash
git checkout dev
```

```bash
git pull origin dev
```

---

# 📤 PUSH CURRENT BRANCH

```bash
git push origin <branch-name>
```

Example:

```bash
git push origin dev
```

---

# 🧹 DELETE FEATURE BRANCH

## Delete Local Branch

```bash
git branch -d feature/sample-loader
```

---

## Delete Remote Branch

```bash
git push origin --delete feature/sample-loader
```

---

# 🧠 IMPORTANT RULES

## NEVER DEVELOP DIRECTLY ON MAIN

Correct:

```plaintext
feature/* → dev → staging → main
```

Wrong:

```plaintext
main → direct coding
```

---

# 🏷️ COMMIT MESSAGE FORMAT

## Feature

```bash
git commit -m "feat: add sample dataset loader"
```

---

## Fix

```bash
git commit -m "fix: resolve upload validation issue"
```

---

## Docs

```bash
git commit -m "docs: update README workflow"
```

---

## Refactor

```bash
git commit -m "refactor: improve analytics pipeline"
```

---

# 📌 CURRENT FEATURE BRANCHES

```plaintext
feature/sample-loader
feature/pdf-export
feature/dynamic-filters
```

---

# 📌 CURRENT BUGFIX BRANCHES

```plaintext
bugfix/chart-rendering
bugfix/upload-validation
bugfix/pdf-generation
```

---

# 🎯 DEVELOPMENT PHILOSOPHY

Focus on:

- usability
- analytics
- reporting
- maintainability
- structured workflows

Avoid:

- overengineering
- unnecessary branches
- premature AI complexity
- feature chaos
