# RESTful API Security Tool 🔒

## Purpose of this document

RESTful API Security Tool is a Python-based RESTful API security testing tool that automates common security testing tasks. The tool uses a modular architecture where the scanner, HTTP engine, payload provider, security modules, data models, and reporting are separated into independent components. The project includes a Docker-based REST API lab and supports CI/CD integration via GitHub Actions.
This document ensures consistency and maintainability across:

- source code;
- the Python package;
- the CLI;
- the Docker lab;
- payloads;
- reports;
- CI/CD;
- project documentation.

---
## 📄 Documentation
* **Detailed Thesis Report:** [Read Full Report on Google Drive](https://drive.google.com/file/d/1R1T9LBEQbhECTE0N9PU7xrOP0H2aNIG1/view?usp=drive_link)

## Project objectives

**RESTful API Security Tool** is a RESTful API security testing tool implemented in Python.

Primary objectives:

- Automate tests for Broken Authentication.
- Detect Excessive Data Exposure.
- Test for SQL Injection (including time-based).
- Fuzz input parameters.
- Analyze HTTP responses and capture evidence.
- Generate reports.
- Support Docker lab deployment and CI/CD integration.
- Designed as modular OOP to facilitate testing, maintenance, and extension.

---

## Project scope

The system focuses on:

```
RESTful API
HTTP / HTTPS
GET / POST and common HTTP methods
URL query parameters
JSON request body
Form request body
Bearer Token
Cookie
SQL Injection
Sensitive-data exposure detection
Authentication checks
Automated reporting
CI/CD integration
```

Intended use:

```
Educational environment
Security laboratory
Research
Authorized security testing
CI/CD security validation
```

Note: The tool is **not** intended to perform post-exploitation or to replace a professional pentesting platform.

---

## Python package structure

Primary package:

```
restful_api_pentest/
```

Proposed layout:

```
restful_api_pentest/
├── __init__.py
├── cli.py
├── config.py
├── context.py
├── http_engine.py
├── logging_utils.py
├── models.py
├── modules.py
├── payloads.py
├── reporter.py
└── scanner.py
```

Each file should have a single responsibility. Module, class and function names must be meaningful and consistent with the documentation.

---

## CLI and entry point

Declare the CLI entry in `pyproject.toml`:

```toml
[project.scripts]
restful-api-pentest = "restful_api_pentest.cli:main"
```

Example usage:

```
restful-api-pentest --help
```

Scan an endpoint:

```
restful-api-pentest -u http://127.0.0.1:5000/api/users --output-dir reports
```

Scan an endpoint with a query parameter:

```
restful-api-pentest -u "http://127.0.0.1:5000/api/search?q=test" -p payloads/sql.txt --output-dir reports
```

---

## CI/CD

Workflow path:

```
.github/workflows/ci.yml
```

Workflow name:

```
name: RESTful API Security Tool - CI
```

Pipeline overview:

```
Checkout source
  ↓
Setup Python
  ↓
Install package
  ↓
Build security lab (Docker)
  ↓
Wait for API
  ↓
Run scans
  ↓
Upload reports
  ↓
Docker cleanup
```

The CLI module used in CI must be `restful_api_pentest.cli`.

---

## CI/CD commands

Scan `/api/users`:

```
python -m restful_api_pentest.cli -u http://127.0.0.1:5000/api/users --output-dir reports
```

Scan for injection:

```
python -m restful_api_pentest.cli -u "http://127.0.0.1:5000/api/search?q=test" -p payloads/sql.txt --output-dir reports
```

Upload reports (GitHub Actions step):

```yaml
- name: Upload reports
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: api-security-reports
    path: reports/
```

Cleanup:

```yaml
- name: Stop API
  if: always()
  run: docker compose down
```

---

## Official repository layout

Suggested repository tree:

```
RESTful API Security Tool/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── payloads/
│   └── sql.txt
│
├── restful_api_pentest/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── context.py
│   ├── http_engine.py
│   ├── logging_utils.py
│   ├── models.py
│   ├── modules.py
│   ├── payloads.py
│   ├── reporter.py
│   └── scanner.py
│
├── security_lab/
│   ├── app.py
│   └── Dockerfile
│
├── tests/
│
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── RENAME.md
└── .gitignore
```

---

## Files that must not be committed

Do not commit:

```
.venv/
reports/
build/
dist/
*.egg-info/
__pycache__/
*.pyc
.pytest_cache/
```

Suggested `.gitignore`:

```
__pycache__/
*.pyc
*.pyo

.venv/
venv/

reports/
report_*.html
report_*.json
report_*.pdf

.pytest_cache/

*.egg-info/
build/
dist/
```

---

## Architectural goals

Responsibilities are separated as:

```
Configuration
  ↓
Payload Management
  ↓
HTTP Engine
  ↓
Scan Context
  ↓
Security Modules
  ↓
Scan Result
  ↓
Reporting
  ↓
CLI / CI/CD
```

Components should be independently extensible.

---

## Development principles

Priorities:

```
Modularity
Maintainability
Testability
Extensibility
Reproducibility
Clear separation of concerns
```

Pattern for adding a new module:

```
SecurityModule
  ↓
NewSecurityModule
  ↓
ModuleFactory
```

HTTP logic should live in `HttpEngine`. Payloads managed via `PayloadProvider`. Reports extended via `ReportGenerator`.

---

## Safety and usage boundaries

Use the tool only on:

- systems owned by the tester;
- controlled lab environments;
- systems with explicit permission for testing;
- controlled CI/CD environments.

Do not use the tool to scan or test systems without authorization. The recommended default for demos and development is the `security_lab/` target.

---


## Demo

**Clone repo — download source**
```bash
git clone <REPOSITORY_URL>
cd "RESTful API Security Tool"
```

**Create and activate virtual environment for Windows PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Create and activate virtual environment for Linux macOS or Git Bash**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Install dependencies and package**
```bash
python -m pip install -r requirements.txt
python -m pip install .
```

**Check CLI is available**
```bash
restful-api-pentest --help
```

**Check Docker is installed and working**
```bash
docker version
```

**Start the lab using docker compose**
```bash
docker compose up -d --build
```

**Check container status**
```bash
docker compose ps
```

**Check API health endpoint**
```bash
curl http://127.0.0.1:5000/health
# expected: {"status":"ok"}
```

**Get users endpoint for demo use cases**
```bash
curl http://127.0.0.1:5000/api/users
```

**Check search endpoint for injection demo**
```bash
curl "http://127.0.0.1:5000/api/search?q=test"
```

**Run demo scan on users endpoint and save reports**
```bash
restful-api-pentest -u http://127.0.0.1:5000/api/users --output-dir reports
```

**Run SQL injection scan using payload file to fuzz parameter q**
```bash
restful-api-pentest -u "http://127.0.0.1:5000/api/search?q=test" -p payloads/sql.txt --output-dir reports
```

**List reports directory**
```bash
ls reports/
```

**Run scan as security gate fail CI on HIGH or CRITICAL findings**
```bash
restful-api-pentest -u http://127.0.0.1:5000/api/users --output-dir reports --fail-on-high
```

**Stop and remove demo environment**
```bash
docker compose down
```

**Verify containers after stopping**
```bash
docker compose ps
```

---

## Troubleshooting

CLI not recognized

```
python -m pip install .
restful-api-pentest --help
```

Docker not running

```
docker version
docker ps
```

API not responding

```
docker compose ps
docker compose logs api
```

Port 5000 is in use

```
# edit docker-compose.yml or stop the process using the port
```

Payload not found

```
ls payloads/sql.txt
```
