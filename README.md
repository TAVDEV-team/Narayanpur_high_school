# Narayanpur High School

REST API and school-management backend for Narayanpur High School. The project is built with Django and Django REST Framework and provides account management, academic records, routines, notices, fund accounting, exam results, report-card PDFs, messages, and a photo gallery.

**Repository:** [TAVDEV-team/Narayanpur_high_school](https://github.com/TAVDEV-team/Narayanpur_high_school)
**Live API documentation:** [Swagger UI](https://narayanpur-high-school.onrender.com/)

## Features

- **Role-based accounts:** students, teachers, headmaster, governing-body members, and office staff
- **JWT authentication:** access and refresh tokens, password changes, and logout
- **School structure:** singleton school profile, classes, batches, subjects, religious/group/extra subject categories, and syllabuses
- **Academic operations:** routines with class and teacher conflict validation, notices with headmaster approval, and school messages
- **Results:** exams, subject marks, grade calculation, class summaries, JSON report cards, and downloadable PDF report cards
- **Fund management:** singleton balance ledger, income and expense transactions, and headmaster-only access
- **Media:** photo categories and photos with local or S3-compatible/Supabase storage
- **API documentation:** generated OpenAPI schema and Swagger UI

## Technology

| Area | Technology |
| --- | --- |
| Language | Python 3.12 |
| Framework | Django 5.2, Django REST Framework |
| Authentication | Simple JWT |
| Database | PostgreSQL |
| Cache | Redis through django-redis |
| API docs | drf-spectacular / Swagger |
| File storage | Local filesystem or S3-compatible storage; Supabase public storage support |
| PDF generation | ReportLab |
| Quality tools | pytest, pytest-django, coverage, Black, Flake8, pre-commit |
| Deployment | Render, Gunicorn, and GitHub Actions |

## Repository layout

```text
Narayanpur_high_school/
├── .github/workflows/
│   └── keepalive.yml              # Periodically pings the Render backend
├── .pre-commit-config.yaml        # Flake8 pre-commit hook
├── Back_end/
│   ├── accounts/                  # Users, roles, profiles, permissions, JWT
│   ├── nphs_school/               # School, classes, batches, subjects, notices,
│   │                              # routines, syllabuses, messages
│   ├── fund/                      # Fund balance and transactions
│   ├── results/                   # Exams, marks, grades, summaries, PDF cards
│   ├── gallery/                   # Photo categories and photos
│   ├── school_backend/            # Django settings, URLs, logging, storage
│   ├── docs/                      # API and branch/contribution documentation
│   ├── manage.py
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── .env.example
└── README.md
```

## API overview

All application routes are rooted under `/api/`.

| Group | Base path | Main resources |
| --- | --- | --- |
| School | `/api/nphs/` | schools, classes, batches, subjects, routines, notices, messages, syllabuses, about |
| Accounts | `/api/user/` | accounts, students, teachers, headmaster, governing body, office helpers |
| Authentication | `/api/user/` | token, refresh, logout, change password |
| Funds | `/api/funds/` | balance, transactions |
| Results | `/api/result/` | exams, results, report cards, PDF report cards, class summaries |
| Gallery | `/api/gallery/` | categories, photos |
| Schema | `/api/schema/` | OpenAPI JSON |
| Swagger | `/` | Interactive Swagger UI |

The API uses JWT Bearer authentication by default. Public endpoints are explicitly assigned by their views, for example result report-card actions. Protected fund routes require the headmaster role.

## Local setup

### Prerequisites

- Python 3.12
- PostgreSQL
- Redis
- A virtual-environment tool

### 1. Clone and enter the backend

```bash
git clone https://github.com/TAVDEV-team/Narayanpur_high_school.git
cd Narayanpur_high_school/Back_end
```

### 2. Create and activate a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Required general settings:

| Variable | Purpose | Example |
| --- | --- | --- |
| `SECRET_KEY` | Django secret key | A securely generated random value |
| `DEBUG` | Django debug mode | `True` locally, `False` in production |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `127.0.0.1,localhost` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins | `https://127.0.0.1,https://localhost` |
| `DATABASE_NAME` | PostgreSQL database name | `narayanpur` |
| `DATABASE_USER` | PostgreSQL user | `postgres` |
| `DATABASE_PASSWORD` | PostgreSQL password | Your local/database password |
| `DATABASE_HOST` | PostgreSQL host | `127.0.0.1` |
| `DATABASE_PORT` | PostgreSQL port | `5432` |
| `REDIS_DATABASE` | Redis cache URL | `redis://127.0.0.1:6379/1` |
| `SUPABASE_URL` | Supabase project URL used for public media URLs | `https://example.supabase.co` |

Optional settings:

| Variable | Purpose |
| --- | --- |
| `LOG_LEVEL` | Logging level; defaults to `INFO` |
| `RENDER` | Set when running on Render |
| `USE_S3` | Enable S3-compatible storage; defaults to `False` |
| `AWS_ACCESS_KEY_ID` | S3/Supabase storage access key |
| `AWS_SECRET_ACCESS_KEY` | S3/Supabase storage secret key |
| `AWS_STORAGE_BUCKET_NAME` | Storage bucket name |
| `AWS_S3_REGION_NAME` | Storage region |
| `AWS_S3_ENDPOINT_URL` | S3-compatible endpoint URL |

The `.env.example` file includes the core database and cache settings plus placeholders for optional S3-compatible storage.

### 5. Prepare PostgreSQL

Create a PostgreSQL database and user matching `DATABASE_*`, then run migrations:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

- Swagger UI: `http://127.0.0.1:8000/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Authentication

Obtain a token:

```http
POST /api/user/token/
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

Use the returned access token:

```http
Authorization: Bearer <access-token>
```

Other authentication endpoints:

- `POST /api/user/token/refresh/`
- `POST /api/user/logout/`
- `POST /api/user/change-password/`

Access tokens expire after 3 minutes and refresh tokens after 30 days.

## Data model highlights

- `Account` is linked one-to-one with Django's `User` and stores mobile number, date of birth, religion, gender, address, joining date, active state, and role.
- `StudentAccount` adds batch, roll number, academic group, and subject assignments.
- `TeacherAccount` adds a base subject and optional class-teacher assignment.
- `HeadMasterAccount` is a singleton pointing to the appointed headmaster teacher.
- `School` is a singleton containing the institution name, code, motto, logo, address, email, and phone.
- `AClass` supports grades 6–10, academic groups, and compulsory, group, religious, and extra subjects.
- `Routine` prevents duplicate class slots and double-booking of a teacher.
- `Notice` has unique-per-date titles, auto-generated slugs, activation state, and headmaster approval tracking.
- `Fund` is a singleton balance computed from income and expense transactions.
- `Result` validates marks against subject limits and class subjects and enforces one result per student, subject, and exam.
- `Photo` and `PhotoCategory` provide the media gallery.

## Testing and quality

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=. --cov-report=term
```

Run Django checks and migration checks:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
```

Run format and lint tools:

```bash
black --check .
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
pre-commit run --all-files
```

CI is configured for Python 3.12 and PostgreSQL 16. Pull requests validate migrations, Django configuration, formatting, fatal Flake8 errors, test coverage, branch names, and commit-message format.

## CI/CD

- `.github/workflows/keepalive.yml` pings the deployed `/api/nphs/routine/` endpoint every 10 minutes.
- `Back_end/.github/workflows/ci.yml` runs tests and repository quality checks for pushes and pull requests targeting `main` or `dev`.
- `Back_end/.github/workflows/ci_deploy.yml` runs tests, linting, and a Render deploy-hook request after pushes to `main`.

The CI workflows assume the backend is the working directory where `manage.py`, `requirements.txt`, and the Django apps are located.

## Contribution

See `Back_end/docs/contribution-guide.md` and `Back_end/docs/branch_management.md` for the repository workflow.

The CI branch-name rule expects:

```text
<type>/<issue-number>-<short-description>
```

Valid branch types are `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, and `style`.

Commit messages validated by CI use:

```text
<type>: <description>
```
# Narayanpur_high_school
