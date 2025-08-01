
# 🧠 Branch Management Guidelines

When working in a team, Git branches can pile up fast like junk drawers. To keep things clean, scalable, and sane, follow these branch management best practices.

---

## 🧩 Branch Types & Lifespan

| Branch Type      | Keep?           | Notes                                               |
|------------------|-----------------|-----------------------------------------------------|
| `main` / `master`| ✅ Yes          | Production-ready, stable code only. Only maintainers push here. |
| `dev` / `develop`| ✅ Yes          | Integration branch for ongoing development. All features and fixes merge here before production. |
| `feature/*`      | 🔁 Until Merged | New feature work. Delete branch after PR merge.     |
| `bugfix/*`       | 🔁 Until Merged | Bug fixes. Same cleanup as features.                 |
| `hotfix/*`       | 🔁 Until Merged | Emergency fixes for production. Merge to both `main` and `dev`. Delete after merge. |
| `chore/*`        | ❌ Only if active | Maintenance, updates, config changes. Clean up when done. |
| `refactor/*`     | 🔁 Until Merged | Code restructuring or improvements without behavior changes. Treat like features. |
| `experiment/*`   | ⚠️ Maybe        | Experimental or spike work. Keep only if valuable; otherwise delete. |
| `backup/*`       | ❌ Temporary    | Temporary backups only. Avoid long-term storage here. |

---

## 🧼 Branch Cleanup Rules

- ✅ **After merging a PR**, delete your feature, bugfix, refactor, hotfix, and chore branches to keep the repo clean.
- ⚠️ **Review stale branches** (no commits for >30 days). Archive or delete them if abandoned.
- ❌ **Avoid keeping dead or WIP branches** that no one plans to continue.

---

## 🛠 Useful Git Commands

```bash
# List branches merged into the current branch (safe to delete)
git branch --merged

# Delete a local branch
git branch -d branch-name

# Force delete local branch (if not merged)
git branch -D branch-name

# Delete a remote branch
git push origin --delete branch-name
````

---

## 🌟 Tips for Smooth Branching

* Always branch off the latest `dev` or `main` to avoid merge hell.
* Keep branches focused: one task, one branch.
* Write clear commit messages mentioning the issue number (e.g., `refactor #45: improve logging`).
* Open PRs early to get feedback and avoid surprises.
* Delete branches after merging to keep repo tidy.

---

By following these, your team repo stays clean, collaboration stays smooth, and nobody loses their mind over git chaos.

---

> Need help or have questions? Ping Mamun anytime.

```

