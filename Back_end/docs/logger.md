

# 📝 Logger Setup & Usage Guide

Logging isn’t just nice to have — it’s **your first responder** for debugging, monitoring, and tracking what’s *really* happening inside your app. This guide walks you through **our logger setup** and how to use it like a pro.

---

## 🎯 Why Use Custom Loggers?

✅ Isolate logs per app/module
✅ Filter by log level (`DEBUG`, `INFO`, `ERROR`, etc.)
✅ Direct logs to files, terminals, or third-party tools
✅ Boost observability and cut debugging time in half

---

## ⚙️ Logger Configuration (In `settings.py`)

We use Django’s `LOGGING` config to:

* 📺 Show Django logs in the console
* 🗃️ Save app-specific logs (like `university`, `payments`, etc.) in `logs/`
* 🧼 Use clear formatting with timestamps and context

### Example:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{name}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'university_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/university.log',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        # ➕ Add more handlers for other apps if needed
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'university': {
            'handlers': ['university_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # ➕ Add more loggers (e.g., 'payments', 'departments')
    },
}
```

---

## 🚀 Using the Logger in Your App

In your app module (e.g., `university/views.py`):

```python
import logging

logger = logging.getLogger('university')

def some_function():
    logger.debug('🐛 Starting function logic')
    try:
        # your logic
        logger.info('✅ Successfully completed logic')
    except Exception as e:
        logger.error(f'❌ Exception occurred: {e}', exc_info=True)
```

---

## ✅ Best Practices

* **Use correct log levels**:

  * `DEBUG`: Internal dev/debug info
  * `INFO`: Normal ops/events
  * `WARNING`: Unexpected but not breaking
  * `ERROR`: Broken logic that needs fixing
  * `CRITICAL`: System failure/emergency

* **Don't log sensitive data**: no passwords, tokens, etc.

* **Use `exc_info=True`** for tracebacks on exceptions

* **Avoid spammy logs**: make logs informative, not noisy

* **Use `RotatingFileHandler`** if log size is a concern

---

## 🔥 Quick Start Checklist

* [ ] Add your logger in `settings.py`
* [ ] Create `logs/` folder (with proper permissions)
* [ ] Use `getLogger('app_name')` in modules
* [ ] Use meaningful logs at appropriate levels
* [ ] Monitor logs weekly (or auto-monitor in prod)

---

## 📚 Resources

* [Django Logging Docs](https://docs.djangoproject.com/en/stable/topics/logging/)
* [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
* [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

---

# 📦 `logger.py` — Reusable Logger Module

This drop-in module gives you:

* ✅ Rotating file-based logging (5MB chunks, 3 backups)
* ✅ Pretty formatting for both file + terminal
* ✅ One-liner logger instancing: `get_logger(__name__)`
* ✅ Emojis for expressive and easy-to-read logs 😎

---

### 🔧 Usage Example

```python
from logger import get_logger

logger = get_logger(__name__)

logger.info("ℹ️ App initialized")
logger.warning("⚠️ Disk space low")
logger.error("❌ DB connection failed")
```

---

## 📘 Emoji Logging Cheat Sheet

| Level    | Emoji(s)       | Use For                                   |
| -------- | -------------- | ----------------------------------------- |
| DEBUG    | 🐛 🔍 🧠 🛠️   | Internal state, values, dev-only insights |
| INFO     | ℹ️ ✅ 📘 🪄     | General operations, success flow          |
| SUCCESS  | 🎉 🟢 🚀 💯 ✅  | Confirmed tasks, milestone completions    |
| WARNING  | ⚠️ 🟡 👀 🫣 🚧 | Potential issues, not breaking yet        |
| ERROR    | ❌ 🔴 💥 🧨 🛑  | Actual problems needing attention         |
| CRITICAL | 💣 🚨 🔥 😱 💀 | Fatal bugs, crashes, outages              |

---

### 🎯 Context-Based Emojis

| Context         | Emoji(s)    |
| --------------- | ----------- |
| API Requests    | 🌐 📲 📡    |
| Database        | 🗄️ 💾 📦   |
| Authentication  | 🔐 🧑‍💻 🪪 |
| File System     | 📁 📝 📂    |
| Timers / Delays | ⏳ ⏰ 🕒      |
| Start / Init    | 🟢 🚀 🛫    |
| Exit / Shutdown | 🔚 🛑 👋    |
| Network / Proxy | 🌍 🧱 🕸️   |
| Retry / Looping | 🔁 ♻️ 🔄    |

---

> 💡 Logging isn’t optional — it’s a **non-negotiable habit of top engineers**.
> Stay sharp. Log smart. Fix fast.

