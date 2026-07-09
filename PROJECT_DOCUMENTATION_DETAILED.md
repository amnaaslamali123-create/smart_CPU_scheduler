# Smart CPU Scheduler - Detailed Project Explanation

This file explains the project structure, what each file does, and how the scheduling algorithms are used. It is written so you can explain the project step-by-step.

## Project Overview

The Smart CPU Scheduler is a Python GUI application that simulates CPU scheduling algorithms. The user can enter process data, select an algorithm, run the simulation, and view results.

The main files are:
- `main.py`
- `gui.py`
- `scheduler.py`
- `algorithms.py`
- `process.py`
- `ai_scheduler.py`
- `utils.py`
- `data/sample_processes.json`

---

## main.py

`main.py` is the program entry point.

1. `from gui import main`
   - Imports the `main` function from `gui.py`.
2. `if __name__ == "__main__":`
   - Ensures the file only runs when the script is executed directly, not when imported.
3. `main()`
   - Starts the application by calling `main()` from `gui.py`.

This file does not contain scheduling logic. It simply launches the GUI.

---

## gui.py

`gui.py` builds the graphical interface and connects user actions to the scheduling logic.

### Important parts

- `SmartCPUSchedulerApp` class:
  - Creates the window and controls.
  - Manages the process table and results display.

- `build_ui(self)`:
  - Sets up the title, subtitle, input fields, buttons, and the process table.
  - Creates fields for number of processes, quantum, algorithm choice, and buttons.
  - Uses a `ttk.Treeview` to display process rows.
  - Binds double-click to edit a table cell.

- `add_process_row(self)`:
  - Reads the number of processes from `process_count_var`.
  - Clears the table and creates new empty rows.
  - Sets default process IDs `P1`, `P2`, `P3`, etc.
  - Leaves arrival, burst, and priority cells empty for the user to fill.

- `load_sample_data(self)`:
  - Loads sample process data from `data/sample_processes.json` using `load_sample_data()` from `utils.py`.
  - Fills the table with pre-defined processes.

- `run_simulation(self)`:
  - Reads the quantum value.
  - Reads each row from the tree table.
  - Converts arrival time and burst time to floats, and priority to int.
  - Creates `Process` objects with these values.
  - Calls `run_selected_algorithm()` from `scheduler.py`.
  - Shows the result summary.

- `on_double_click(self, event)` and `commit_edit(self, event)`:
  - Allow the user to edit table cells by double-clicking.
  - Commit the edited cell back into the table.

- Output buttons:
  - `Show Gantt Chart` shows a timeline chart.
  - `Compare Algorithms` runs all algorithms and compares them.
  - `AI Recommendation` chooses the best algorithm based on heuristics.
  - `Save JSON` writes results to `results.json`.
  - `Export PDF` writes results to `results.pdf`.

### What this file does

1. Displays the UI.
2. Collects user-entered process inputs.
3. Validates input values.
4. Sends process list and selected algorithm to `scheduler.py`.
5. Shows results and lets the user compare or save them.

---

## scheduler.py

`scheduler.py` decides which scheduling algorithm to run.

### Key functions

- `run_selected_algorithm(processes, algorithm, quantum)`:
  - Clones the process list with `clone_processes()` so algorithms do not change the original input.
  - Checks the algorithm name and calls the correct function from `algorithms.py`.
  - Supports "FCFS", "SJF", "SRTF", "Priority Scheduling", "Round Robin", and "Compare All".

- `compare_algorithms(processes, quantum)`:
  - Runs all algorithms and returns a comparison dictionary.
  - Includes results for FCFS, SJF, SRTF, Priority Scheduling, and Round Robin.

### What this file does

This file is the routing layer: it chooses the correct algorithm code and executes it.

---

## algorithms.py

`algorithms.py` contains the actual scheduling algorithm implementations and result processing.

### Shared helper functions

- `_finalize_metrics(processes, finish_time)`:
  - Sets `completion_time` for any process that still has 0.0 completion time.
  - Computes `turnaround_time = completion_time - arrival_time`.
  - Computes `waiting_time = turnaround_time - burst_time`.
  - Ensures `response_time` is set to 0.0 if it was never assigned.

- `_build_result(processes, timeline, algorithm_name)`:
  - Calculates average waiting time, turnaround time, and response time.
  - Calculates CPU utilization and throughput.
  - Packages results in a dictionary.

### Algorithm implementations

1. `fcfs(processes)`
   - First Come First Serve.
   - Sorts processes by `arrival_time` and `pid`.
   - Runs each process in arrival order.
   - `response_time` is when the process starts minus arrival.
   - `completion_time` is current time after finishing the burst.

2. `sjf_non_preemptive(processes)`
   - Shortest Job First, non-preemptive.
   - At each step, it selects the process with the smallest burst time among arrived processes.
   - If no process has arrived yet, the scheduler jumps to the next arrival time.
   - Once a process starts, it runs until completion.

3. `srtf(processes)`
   - Shortest Remaining Time First, preemptive.
   - Repeatedly picks the arrived process with the smallest remaining time.
   - Can preempt the running process when a new process arrives with shorter remaining time.
   - Tracks partial execution and updates the timeline for each run slice.

4. `priority_scheduling(processes)`
   - Sorts by `arrival_time`, then `priority`, then `pid`.
   - Lower numeric `priority` means higher importance.
   - Runs processes in that order, without preemption.

5. `round_robin(processes, quantum)`
   - Uses a queue and gives each process a time slice of `quantum`.
   - If a process does not finish in one slice, it goes to the end of the queue.
   - Continues until all processes are complete.

### What this file does

This file contains the actual CPU scheduling algorithm logic and returns the final metrics.

---

## process.py

`process.py` defines the `Process` data model.

### `Process` class

Fields:
- `pid`: process ID string like "P1".
- `arrival_time`: when the process arrives.
- `burst_time`: CPU time needed.
- `priority`: priority number.
- `waiting_time`: calculated later.
- `turnaround_time`: calculated later.
- `completion_time`: calculated later.
- `response_time`: first time the process starts.
- `remaining_time`: initialized from `burst_time`.

Methods:
- `__post_init__`: sets `remaining_time = burst_time`.
- `to_dict()`: returns process data as a dictionary.
- `from_dict(item)`: creates a `Process` from JSON data.

- `clone_processes(processes)`:
  - Copies process objects so algorithms can run without modifying the original list.

### What this file does

This file stores process properties and helps clone them for safe simulation.

---

## ai_scheduler.py

`ai_scheduler.py` recommends the best algorithm for the current workload.

### `recommend_best_algorithm(processes, quantum)`

1. Collects candidate algorithms based on process properties:
   - If there are 6 or more processes, it considers Round Robin.
   - If any process has priority values not equal to 0, it considers Priority Scheduling.
   - If there are arrival times later than 0 and 4 or more processes, it considers SRTF.
   - If there are 4 or fewer processes and all arrival times are 0, it considers SJF.
   - If no special case applies, it defaults to FCFS.

2. Runs each candidate algorithm and records results.
3. Sorts the candidate results by:
   - Average waiting time
   - Average turnaround time
   - Average response time
4. Returns the best algorithm name, its result, and a reason.

### What this file does

This file chooses the best algorithm using simple heuristics and result comparison.

---

## utils.py

`utils.py` contains simple helper functions.

### Functions

- `load_sample_data()`:
  - Loads `data/sample_processes.json`.
  - Returns a list of `Process` objects.

- `save_results_json(path, data)`:
  - Saves the simulation result dictionary to a JSON file.

- `export_to_pdf(path, content)`:
  - Writes content to a file named `results.pdf`.
  - In this project, it is a simple text file saved with `.pdf` extension.

### What this file does

This file handles file I/O for sample data and result export.

---

## data/sample_processes.json

Contains example process data with:
- `pid`
- `arrival_time`
- `burst_time`
- `priority`

This file is loaded when the user clicks "Load Sample Data".

---

## How algorithms are executed in the app

1. The user enters process details in the table.
2. The user selects an algorithm from the dropdown.
3. The app collects process rows and creates `Process` objects.
4. `gui.py` calls `run_selected_algorithm()` in `scheduler.py`.
5. `scheduler.py` runs the correct algorithm from `algorithms.py`.
6. The chosen algorithm simulates process execution and computes metrics.
7. Results are shown in the text output area.

If the user chooses "Compare Algorithms", all algorithms run and the app shows a summary for each.

If the user chooses "AI Recommendation", the app uses `ai_scheduler.py` to recommend the best algorithm based on process count, arrival times, and priorities.

---

## How to explain the project in your presentation

- Start with `main.py`: this is the app launch file.
- Explain `gui.py`: it builds the UI and lets the user enter process values.
- Explain `scheduler.py`: it chooses which scheduling algorithm to use.
- Explain `algorithms.py`: it contains the scheduling strategies.
- Explain `process.py`: it stores process data and cloning logic.
- Explain `ai_scheduler.py`: it selects the best algorithm automatically.
- Mention `utils.py`: it loads sample data and saves results.
- Use examples:
  - `FCFS` executes processes by arrival order.
  - `SJF` chooses the shortest burst among arrived processes.
  - `SRTF` can switch processes when a shorter one arrives.
  - `Priority Scheduling` chooses by priority value.
  - `Round Robin` rotates processes using quantum.

This file gives you the explanations in one place for your project demo.
