# 🌦️ WeatherAI API Test Automation Framework

> **Python-based API test automation framework for testing and validating the WeatherAI API.**

Built with **Python, Pytest, Requests, and pytest-html**, this framework validates API functionality, error handling, input validation, response structure, data quality, authentication, parameter behavior, and basic performance.


## 📊 Test Suite Overview

<table>
<tr>
<td><strong>Framework</strong></td>
<td>Pytest</td>
</tr>
<tr>
<td><strong>Language</strong></td>
<td>Python 3.13+</td>
</tr>
<tr>
<td><strong>HTTP Client</strong></td>
<td>Requests</td>
</tr>
<tr>
<td><strong>Reporting</strong></td>
<td>pytest-html</td>
</tr>
<tr>
<td><strong>Configuration</strong></td>
<td>python-dotenv</td>
</tr>
<tr>
<td><strong>Tests</strong></td>
<td><strong>39</strong></td>
</tr>
<tr>
<td><strong>API Performance Threshold</strong></td>
<td>5 seconds</td>
</tr>
<tr>
<td><strong>CI Ready</strong></td>
<td>GitHub Actions</td>
</tr>
</table>

## 🎯 1. Project Overview

This project demonstrates a structured approach to **API test automation** against the WeatherAI API.

### The test suite covers

* ✅ Happy-path API requests
* ✅ HTTP response status codes
* ✅ Response structure and JSON validation
* ✅ Weather data quality
* ✅ Multiple geographic locations
* ✅ Latitude and longitude validation
* ✅ Boundary values
* ✅ Missing parameters
* ✅ Invalid parameter types
* ✅ Authentication
* ✅ Forecast-day handling
* ✅ Units handling
* ✅ Optional API parameters
* ✅ Unknown parameters
* ✅ API response time
* ✅ Edge cases

### Framework objectives

| Objective              | Status |
| ---------------------- | ------ |
| Readable               | ✅      |
| Maintainable           | ✅      |
| Reproducible           | ✅      |
| Easy to run locally    | ✅      |
| CI compatible          | ✅      |
| Secure API credentials | ✅      |

---

## 🛠️ 2. Technology Stack

| Technology        | Purpose                                |
| ----------------- | -------------------------------------- |
| **Python 3.13+**  | Programming language                   |
| **Pytest**        | Test framework                         |
| **Requests**      | HTTP/API requests                      |
| **pytest-html**   | HTML test reporting                    |
| **python-dotenv** | Environment variable management        |
| **Git / GitHub**  | Version control and repository hosting |

Dependencies are defined in:

```text
requirements.txt
```

---

## 📁 3. Project Structure

```text
WeatherAI-API-Tests/
│
├── .github/
│   └── workflows/
│
├── tests/
│   └── test_weather.py
│
├── utils/
│   └── api_client.py
│
├── reports/
│   └── test-report.html
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> ⚠️ **Security:** `.env` contains the API key and must never be committed to GitHub. The `.gitignore` excludes sensitive configuration and generated reports.

---

## 💻 4. Prerequisites

Before running the tests, install:

* Python 3.13 or later
* Git
* Windows PowerShell

Verify Python:

```powershell
python --version
```

Verify Git:

```powershell
git --version
```

---

## 📥 5. Clone the Repository

Create a workspace folder:

```powershell
mkdir QA-Projects
cd QA-Projects
```

Clone the repository:

```powershell
git clone https://github.com/paulonwonga15/WeatherAI-API-Tests.git
```

Enter the project:

```powershell
cd WeatherAI-API-Tests
```

Verify the project files:

```powershell
Get-ChildItem -Force
```

---

## 🐍 6. Create a Virtual Environment

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

For example:

```text
(.venv) PS C:\...\WeatherAI-API-Tests>
```

> 💡 Make sure `(.venv)` is visible before installing dependencies or running tests.

---

## 📦 7. Install Dependencies

With the virtual environment activated:

```powershell
python -m pip install -r requirements.txt
```

Verify Pytest:

```powershell
python -m pytest --version
```

---

## 🔐 8. Configure the API Key

Create a file named:

```text
.env
```

in the project root.

Add:

```env
WEATHER_API_KEY=your_actual_api_key
```

Replace `your_actual_api_key` with your valid WeatherAI API key.

### Windows / Notepad

If using Notepad:

1. Open Notepad.
2. Enter:

```text
WEATHER_API_KEY=your_actual_api_key
```

3. Select **File → Save As**
4. Set **File name** to:

```text
.env
```

5. Set **Save as type** to:

```text
All Files (*.*)
```

6. Save it in the project root.

Make sure Windows does not create:

```text
.env.txt
```

The application expects:

```text
.env
```

### Verify the file

```powershell
Get-ChildItem -Force .env*
```

If `.env.txt` exists:

```powershell
Rename-Item ".env.txt" ".env"
```

---

## 🔎 9. Verify the API Key

Verify that the environment file loads correctly **without displaying the API key**:

```powershell
python -c "from dotenv import load_dotenv; import os; print('Loaded:', load_dotenv()); print('Key found:', bool(os.getenv('WEATHER_API_KEY')))"
```

Expected:

```text
Loaded: True
Key found: True
```

---

## 🧪 10. Run the Test Suite

Run all tests and generate the HTML report:

```powershell
python -m pytest -v --html=reports/test-report.html --self-contained-html
```

This command:

* Runs all Pytest tests
* Displays detailed results in PowerShell
* Generates an HTML report
* Creates a self-contained report
* Saves it to `reports/test-report.html`

### Expected result

```text
=========================== 39 passed in XX.XXs ===========================
```

Execution time can vary depending on API response times and network conditions.

---

## 📊 11. HTML Test Report

Open the generated report:

```powershell
start reports\test-report.html
```

The HTML report provides:

* Test names
* Pass/fail status
* Execution duration
* Test session information
* Environment information
* Individual test results
* Captured test output

---

# 🧪 12. Test Strategy

The test suite is organized by functional area.

## 🌤️ Core Weather API

Validates:

* Successful weather requests
* Response structure
* Required fields
* Current weather data
* Daily forecast data
* Data types
* Multiple locations
* Weather data quality

## 🔐 Authentication

Validates:

* Invalid API credentials
* Expected unauthorized response

## 🌍 Latitude & Longitude Validation

Validates:

* Out-of-range latitude
* Out-of-range longitude
* Missing latitude
* Missing longitude
* Invalid latitude types
* Invalid longitude types
* Empty latitude
* Empty longitude
* Latitude boundaries
* Longitude boundaries
* Zero coordinates
* Very large coordinates
* Boolean coordinates

## 📅 Forecast Days Validation

Validates:

* Default forecast behavior
* One-day forecasts
* Seven-day forecasts
* Zero days
* Values above the supported maximum
* Negative values
* Invalid types
* Empty values
* Decimal values

## 🌡️ Units Validation

Validates:

* Imperial units
* Invalid unit values
* Empty units
* Case variations

## ⚙️ Optional Parameters / API Contract

Validates:

* Disabling the AI option
* Unknown parameters

## 📄 Response Format

Validates:

* HTTP response content type
* JSON response structure

---

# ⚡ 13. Performance Testing

The suite includes a basic API response-time test.

The current threshold is:

```text
5 seconds
```

The test measures the time required for a standard weather request to receive a response.

> This is a **basic performance check**, not a load or stress-testing solution.

The suite does not intentionally generate large volumes of concurrent requests because the assignment focuses on functional API automation and basic performance validation.

---

# 📈 14. Test Count

The current test suite contains:

## **39 tests**

The suite includes both positive and negative scenarios, with parameterized tests used where appropriate.

---

# 🔧 15. API Client

The API client is located at:

```text
utils/api_client.py
```

The client:

* Loads the API key from `.env`
* Builds the authorization header
* Sends requests to the WeatherAI API
* Accepts latitude and longitude
* Supports additional API parameters
* Uses a request timeout
* Returns HTTP responses for assertions in the test layer

Keeping API request logic separate from the test cases makes the framework easier to maintain.

---

# 🔒 16. Security

API credentials are loaded from environment variables using `python-dotenv`.

The `.env` file must never be committed to GitHub.

The repository `.gitignore` contains:

```text
.venv/
.env
__pycache__/
.pytest_cache/
htmlcov/
*.pyc
reports/
```

If an API key is accidentally exposed publicly, it should be **revoked or rotated immediately**.

---

# 🧩 17. Observed API Behavior

During testing, several input-validation behaviors were identified.

Some invalid inputs are **normalized and return HTTP 200**, while others return **400** or **502**.

The following table documents the behavior observed during testing of the current API implementation.

| Test Case                | Observed Result                                 |
| ------------------------ | ----------------------------------------------- |
| `days=0`                 | **200** — normalized to `7`                     |
| `days=8`                 | **200** — normalized to `7`                     |
| `days=-1`                | **200** — normalized to a valid positive number |
| `days="abc"`             | **200** — normalized                            |
| `days=""`                | **200** — normalized                            |
| `days=3.5`               | **502**                                         |
| `lat=200`                | **502**                                         |
| `lon=250`                | **502**                                         |
| `lat=999999, lon=999999` | **502**                                         |
| Empty `lat`              | **200**                                         |
| Empty `lon`              | **200**                                         |
| `lat=0, lon=0`           | **200**                                         |

> **Note:** These results represent observed behavior of the API during testing and are documented as part of the test automation process.

---

# 🛠️ 18. Troubleshooting

### `No module named pytest`

Make sure the virtual environment is active:

```text
(.venv)
```

Then:

```powershell
python -m pytest -v
```

If necessary:

```powershell
python -m pip install -r requirements.txt
```

---

### `WEATHER_API_KEY is not set`

Check that `.env` exists:

```powershell
Get-ChildItem -Force .env*
```

Expected:

```text
.env
```

If it is `.env.txt`:

```powershell
Rename-Item ".env.txt" ".env"
```

Then verify:

```powershell
python -c "from dotenv import load_dotenv; import os; print('Loaded:', load_dotenv()); print('Key found:', bool(os.getenv('WEATHER_API_KEY')))"
```

Expected:

```text
Loaded: True
Key found: True
```

---

### `python -m pytest` works but `pytest` does not

Use:

```powershell
python -m pytest -v
```

This ensures Pytest is executed using the Python interpreter from the active virtual environment.

---

### HTML report does not open

Verify the report exists:

```powershell
Get-ChildItem reports
```

Then:

```powershell
start reports\test-report.html
```

---

# ✅ 19. Expected Successful Run

A successful test execution should look similar to:

```text
============================= test session starts =============================

collected 39 items

=========================== 39 passed in XX.XXs ===========================
```

The exact execution time may vary depending on network conditions and API response times.

The HTML report is generated at:

```text
reports/test-report.html
```

---

# 🤖 20. CI / Continuous Integration

The framework is structured for integration with **GitHub Actions**.

For CI execution:

* API credentials should be stored as secure repository/environment secrets.
* `.env` should never be committed.
* Tests can be executed automatically on pushes or pull requests.
* HTML reports can be uploaded as CI artifacts.

---

# 🚀 21. Quick Start

```powershell
mkdir QA-Projects
cd QA-Projects

git clone https://github.com/paulonwonga15/WeatherAI-API-Tests.git
cd WeatherAI-API-Tests

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

Create `.env`:

```env
WEATHER_API_KEY=your_actual_api_key
```

Verify:

```powershell
python -c "from dotenv import load_dotenv; import os; print('Loaded:', load_dotenv()); print('Key found:', bool(os.getenv('WEATHER_API_KEY')))"
```

Run tests:

```powershell
python -m pytest -v --html=reports/test-report.html --self-contained-html
```

Open the report:

```powershell
start reports\test-report.html
```

---

# 📌 22. Summary

WeatherAI API Test Automation Framework demonstrates a structured approach to API quality assurance using **Python, Pytest, and Requests**.

### Coverage

| Area                   | Covered |
| ---------------------- | :-----: |
| Functional API Testing |    ✅    |
| Positive Scenarios     |    ✅    |
| Negative Scenarios     |    ✅    |
| Boundary Testing       |    ✅    |
| Input Validation       |    ✅    |
| Authentication         |    ✅    |
| Data Quality           |    ✅    |
| Response Contract      |    ✅    |
| Multiple Locations     |    ✅    |
| Parameter Handling     |    ✅    |
| Performance Check      |    ✅    |
| HTML Reporting         |    ✅    |
| CI Integration         |    ✅    |

---

## 🔗 Repository

**GitHub:**
https://github.com/paulonwonga15/WeatherAI-API-Tests

### Recommended execution

```powershell
python -m pytest -v --html=reports/test-report.html --self-contained-html
```

### Open the report

```powershell
start reports\test-report.html
```

---

<p align="center">
  <strong>WeatherAI API Test Automation</strong><br>
  Built with Python • Pytest • Requests • GitHub Actions
</p>
