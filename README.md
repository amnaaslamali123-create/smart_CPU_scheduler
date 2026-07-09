# Smart CPU Scheduler

A beginner-friendly desktop application for studying CPU scheduling algorithms using Python and Tkinter.

## Project Structure

- main.py: starts the application
- process.py: defines the Process data model
- algorithms.py: implements FCFS, SJF, SRTF, Priority Scheduling, and Round Robin
- scheduler.py: runs single algorithms or compares all of them
- ai_scheduler.py: recommends the most suitable algorithm
- gui.py: creates the desktop interface
- charts.py: draws the Gantt chart and comparison graphs
- utils.py: loads sample data and exports results
- data/sample_processes.json: sample input data
- assets/icons: folder for icons

## Installation

1. Install Python 3.10 or newer.
2. Open the project folder in VS Code.
3. Install the required packages:

```bash
pip install matplotlib
```

## Run the Project

```bash
python main.py
```

## Features

- Home screen for process input
- Multiple scheduling algorithms
- Gantt chart and comparison graphs
- AI recommendation system
- Save results as JSON
- Export results to PDF

## Notes

This project is designed to be easy to learn and extend for academic use.
