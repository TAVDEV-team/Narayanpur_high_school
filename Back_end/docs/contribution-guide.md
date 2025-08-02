
# 🧭 CCN UST - Dev Board Contribution Guide

Welcome to the dev board project! This doc covers **how we work** — from branching and committing to issue creation and pull requests.

---

## 🧱 Branching Strategy

### Permanent Branches:

* **`main`** — Stable, production-ready code. Only maintainers (Mamun) push here.
* **`dev`** — Main development branch. All features, fixes, and chores merge into this.

### Working Branches (Short-Lived):

Create off `dev`. Name them with prefixes:

| Purpose | Prefix     | Example                      |
| ------- | ---------- | ---------------------------- |
| Feature | `feature/` | `feature/user-auth`          |
| Bug Fix | `bugfix/`  | `bugfix/fix-login`           |
| Chore   | `chore/`   | `chore/pep8-accounts`        |
| Docs    | `docs/`    | `docs/update-readme`         |
| Hotfix  | `hotfix/`  | `hotfix/db-connection-error` |
| Refactor  | `refactor/`  | `refactor/authentication-views` |

---

## 🚀 Git Workflow

1. **Switch to `dev` branch**

   ```bash
   git checkout dev && git pull
   ```

2. **Create a new branch**

   ```bash
   git checkout -b feature/task-name
   ```

3. **Make your changes**

4. **Stage your changes**

   ```bash
   git add .         # Or specify files: git add path/to/file
   ```

5. **Commit using the format**

   ```bash
   type #issue: short summary
   ```

6. **Push your branch**

   ```bash
   git push origin feature/task-name
   ```

7. **Create a Pull Request**

   * Target branch: `dev`
   * Clear title and description
   * Link the issue: `Closes #<issue_number>`

---

## ✅ Commit Message Guidelines

Keep commits clean and issues visible with this structure:

```
type #issue: short summary
```

**Common types:**

* `feat` — New feature
* `fix` — Bug fix
* `docs` — Documentation changes
* `chore` — Maintenance or non-functional updates
* `hotfix` — Critical urgent fixes
* `refactor` — Code restructuring without behavior changes
* `test` — Tests added or fixed

### 💡 Examples

* `feat #3: add login API with JWT`
* `fix #5: resolve user session timeout`
* `docs #7: update README with setup instructions`
* `chore #2: apply PEP8 formatting to accounts app`
* `refactor #9: unify logging config across modules`

---

## 🔄 Pull Requests (PR)

* **Target branch:** `dev` only (never `main`)
* **Title:** Clear & concise
* **Description:**

  * What you did
  * Why you did it
  * How to test (if applicable)
* **Link the issue:** `Closes #<issue_number>`

PRs are reviewed before merging. Only lead (Mamun) merges to `main`.

---

## 🐛 Issue Creation

Every task, bug, or improvement starts as an **Issue**.

### Issue Template:

```
## 📝 Task
Brief description of the task.

## 📂 Affected Areas
List files/modules impacted.

## 🔧 Tools
(Optional) Tools or libs to use (e.g. black, isort).

## ✅ Done When
- Clear completion criteria.

Tag: (feature, bug, chore, docs)
```

### Example Issue:

```
#2 Apply PEP8 formatting to accounts app

## 📝 Task
Format code in `accounts/` folder to follow PEP8 standards.

## 📂 Affected Areas
- accounts/views.py
- accounts/forms.py

## 🔧 Tools
- black
- isort

## ✅ Done When
- All files formatted by black/isort
- No behavior changes
- PR created & linked to this issue
```

---

💡 **Need help?** Ask Mamun or open an issue tagged `question`.

---
