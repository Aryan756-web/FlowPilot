# FlowPilot

FlowPilot is a Python-based task management and productivity tracking application. It helps users organize their tasks, manage deadlines, track time, and understand their productivity.

## Features

* Create, view, update, and delete tasks
* Set task priorities and deadlines
* Track estimated and actual working hours
* Save tasks locally using JSON
* View productivity statistics
* Identify overdue tasks
* Compare estimated time with actual time
* Analyze tasks by priority
* Export task and productivity reports to CSV
* Run automated tests

## Technologies Used

* Python
* Pandas
* JSON
* CSV
* unittest

## How to Run

**1. Create a virtual environment**

```powershell
python -m venv .venv
```

**2. Activate the virtual environment**

```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```powershell
python -m pip install -r requirements.txt
```

**4. Start the application**

```powershell
python -m app.main
```

## Running Tests

Run the following command to execute the automated tests:

```powershell
python -m unittest discover -s tests -v
```

The project currently has 33 passing automated tests.

## Project Structure

The project is organized into a few main folders:

* `app/` — Contains the application code.
* `app/models/` — Defines the task model.
* `app/services/` — Handles task management, storage, and reports.
* `app/analytics/` — Calculates productivity statistics.
* `data/` — Stores task data.
* `reports/` — Stores exported reports.
* `tests/` — Contains automated tests.

The project also includes `requirements.txt` for dependencies, `.gitignore` for excluding unnecessary files, and `README.md` for documentation.

## Productivity Calculations

**Time variance:** The difference between actual hours and estimated hours. A negative value means the task took less time than expected.

**Time efficiency:** Compares estimated hours with actual hours. A value above 100% means the task took less time than estimated.

**Overdue tasks:** Tasks with deadlines before the current date that have not been completed.

## Project Status

FlowPilot currently supports task management, JSON-based data storage, productivity analysis, and CSV report generation. All 33 automated tests are passing.

The project is built as a command-line application, with opportunities to add a graphical interface, database integration, and more advanced analytics in the future.
