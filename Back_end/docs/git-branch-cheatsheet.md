

# 🧠 Git Branch Types Cheat Sheet

**For team projects & clean workflows**

---

## 🔧 Branch Prefixes

| Prefix      | Purpose                             | When to Use                                                       |
| ----------- | ----------------------------------- | ----------------------------------------------------------------- |
| `feature/`  | 🚀 New features                     | Adding something brand new (e.g. login, search, dark mode)        |
| `bugfix/`   | 🐛 Fixing bugs                      | Fixing a known issue or unexpected behavior                       |
| `hotfix/`   | 🔥 Emergency production fix         | Fixing a crash or critical error on live/production version       |
| `docs/`     | 📚 Documentation changes            | Editing README, API docs, or other markdown/doc files             |
| `chore/`    | 🧹 Non-functional, dev-only updates | Refactoring, config changes, dependency updates, cleanup          |
| `refactor/` | 🔄 Code restructuring               | Improving code structure or readability without changing behavior |

---

## 🔍 Detailed Explanation

### ✅ `feature/`

* **Use when**: You’re adding a new functionality.
* **Examples**:

  * `feature/signup-page`
  * `feature/user-profile`
* **Merge into**: `develop` or `main` via PR

---

### 🐞 `bugfix/`

* **Use when**: You're fixing a bug that affects expected behavior.
* **Examples**:

  * `bugfix/navbar-scroll`
  * `bugfix/form-validation`
* **Merge into**: `develop`

---

### 🔥 `hotfix/`

* **Use when**: You're fixing a critical issue that needs to go live **ASAP**.
* **Examples**:

  * `hotfix/login-error-prod`
  * `hotfix/payment-failure`
* **Merge into**: `main` and `develop`

---

### 📖 `docs/`

* **Use when**: You're editing or adding documentation.
* **Examples**:

  * `docs/readme-update`
  * `docs/api-guide`
* **Merge into**: `develop` or `main`

---

### 🧹 `chore/`

* **Use when**: You're doing background setup or dev housekeeping.
* **Examples**:

  * `chore/setup-eslint`
  * `chore/update-dependencies`
* **Merge into**: `develop`

---

### 🔄 `refactor/`

* **Use when**: You’re restructuring or cleaning up code **without** changing behavior.
* **Examples**:

  * `refactor/unify-logging-config`
  * `refactor/simplify-auth-middleware`
* **Merge into**: `develop`

---

## 🌈 Branch Naming Style

Use **kebab-case** (all lowercase, hyphens between words) for readability:

```
feature/add-user-auth
bugfix/fix-header-alignment
docs/improve-readme
refactor/simplify-auth-middleware
```

---

## 💡 Pro Tips

* Keep branches small and focused: 1 task = 1 branch.
* Always create from the latest `develop` or `main`.
* Open a Pull Request as soon as you're ready for review.
* Delete branches after merging to keep the repo clean.

---
