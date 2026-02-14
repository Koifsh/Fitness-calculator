# Fitness Calculator

A desktop fitness tracking application built with **PyQt5** and **SQL Server**, designed to help users log workouts, visualize training progress, and calculate key performance metrics.

## Features

- **User Authentication** — Create an account or log in with device-based session persistence ("Remember Me")
- **Workout Logging** — Record exercises with sets, reps, and weight; supports both strength and cardio entries
- **One-Rep Max Calculator** — Estimates your 1RM by averaging the Brzycki, Epley, and Lander formulas
- **Data Visualization** — Interactive Matplotlib graphs for Volume, Weight, Speed, Distance, and Time, filterable by exercise
- **Metric & Imperial Units** — Toggle between measurement systems at any time; values are stored and converted automatically
- **Customizable Themes** — Full color picker for background, accent, primary, secondary, and text colors with persistent style storage
- **Exercise Autocomplete** — Searchable dropdown with a bundled exercise database (strength & cardio categories)

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| GUI          | PyQt5                               |
| Database     | SQL Server (via SQLAlchemy + pyodbc) |
| Data         | pandas                              |
| Graphing     | Matplotlib                          |
| Styling      | CSS-based Qt stylesheets + JSON     |

## Getting Started

### Prerequisites

- Python 3.10+
- SQL Server with ODBC Driver 17
- Required Python packages:

```
pip install PyQt5 pandas sqlalchemy pyodbc matplotlib
```

### Running

```bash
python main.py
```

> **Note:** On first launch the app will generate a unique device ID and attempt to connect to the configured SQL Server instance. Update the connection string in `main.py` if your server details differ.

## Project Structure

```
├── main.py          # Application entry point and all screen/logic definitions
├── tools.py         # Reusable PyQt5 widget classes (Button, LineEdit, Text, etc.)
├── sort.py          # Utility script to sort the exercise CSV
├── data/
│   └── excercises.csv   # Bundled exercise database
└── styles/
    ├── style.css            # Qt stylesheet template
    └── defaultstyle.json    # Default color palette
```

## License

This project is provided as-is for personal use.
