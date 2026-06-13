# Python Playwright BDD

End-to-end test automation framework migrated from the original TypeScript Playwright BDD project to Python.

The project uses:
- [Playwright for Python](https://playwright.dev/python/) for browser automation
- [pytest](https://docs.pytest.org/) as the test runner
- [pytest-bdd](https://pytest-bdd.readthedocs.io/) for Gherkin scenarios
- [python-dotenv](https://pypi.org/project/python-dotenv/) for environment configuration

## Prerequisites

Install:
- Python 3.10 or newer
- Git
- Visual Studio Code, optional

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/ArtemOganesyan/typescript-playwright-bdd.git
cd typescript-playwright-bdd
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies and Playwright browsers:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install
```

Create local environment settings:

```bash
cp .env.example .env
```

## Configuration

Configuration is loaded from `.env` by `config.py`.

Important variables:
- `BROWSER`: `chromium`, `firefox`, or `webkit`
- `HEADLESS`: `true` or `false`
- `SLOW_MO`: delay in milliseconds between Playwright actions
- `VIEWPORT_WIDTH`, `VIEWPORT_HEIGHT`: browser viewport size
- `GLOBAL_TIMEOUT`, `ACTION_TIMEOUT`, `NAVIGATION_TIMEOUT`, `EXPECT_TIMEOUT`, `WAIT_TIMEOUT`: timeouts in milliseconds
- `TEST_QUOTE_BASE_URL`: URL for the classic pytest scaffold test

## VS Code Settings

The repository includes `.vscode/settings.json` so VS Code can discover Python tests and BDD steps:

```json
{
  "cucumber.features": [
    "bdd/features/**/*.feature"
  ],
  "cucumber.glue": [
    "bdd/steps/**/*.py"
  ],
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

Recommended VS Code extensions:
- Python by Microsoft
- Cucumber by Cucumber.io

After changing extension or workspace settings, run `Developer: Reload Window` in VS Code.

## Running Tests

Run all tests:

```bash
pytest
```

Run only BDD tests:

```bash
pytest -m bdd
```

Run the nopCommerce demo BDD scenario:

```bash
pytest -m bdd1
```

Run a single test file:

```bash
pytest tests/test_bdd.py
```

Run tests by name:

```bash
pytest -k "Featured"
```

## Recording Tests

The Microsoft Playwright Test extension for VS Code discovers JavaScript/TypeScript Playwright Test projects. This project uses Python, pytest, and pytest-bdd, so the extension can show `no playwright tests found` when using its Record button.

Use Python Playwright codegen instead:

```bash
python record.py
```

By default this opens `https://nop-qa.portnov.com/` and saves generated pytest code to `tests/recorded_test.py`.

You can also run codegen directly:

```bash
python -m playwright codegen --target python-pytest --output tests/recorded_test.py https://nop-qa.portnov.com/
```

In VS Code, run the task `Record Python Playwright test` from `Terminal -> Run Task`.

## Reports And Artifacts

HTML report:

```bash
open test-reports/report.html
```

On Windows:

```powershell
start test-reports/report.html
```

Runtime artifacts are written to:
- `test-reports/report.html`
- `test-reports/videos/`
- `test-reports/screenshots/` for failed tests
- `test-results/` when Playwright creates additional artifacts

## Project Structure

```text
.
├── bdd/
│   ├── features/
│   │   └── bdd.feature
│   └── steps/
│       └── bdd_steps.py
├── tests/
│   ├── test_bdd.py
│   └── test_quote_form.py
├── config.py
├── conftest.py
├── pytest.ini
├── requirements.txt
└── .env.example
```

## Notes

The original repository contained an empty TypeScript Playwright quote-form test. In this Python version it remains as a lightweight scaffold that opens `TEST_QUOTE_BASE_URL` and verifies that the page loads with a title.

The BDD scenario uses `https://nop-qa.portnov.com/`. It verifies featured products and prices, opens a product details page, checks availability, and searches for `computer`.
