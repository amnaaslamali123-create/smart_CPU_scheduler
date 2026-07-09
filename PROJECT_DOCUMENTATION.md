# Smart CPU Scheduler – Project Documentation

## 1. What this project does

This application helps students and beginners understand how CPU scheduling algorithms work.
It shows how different algorithms handle processes, compares their performance, and recommends the best one for a given workload.

## 2. Files in the project

- [main.py](main.py): starts the application.
- [process.py](process.py): defines the Process class.
- [algorithms.py](algorithms.py): contains FCFS, SJF, SRTF, Priority, and Round Robin logic.
- [scheduler.py](scheduler.py): runs one algorithm or compares all algorithms.
- [ai_scheduler.py](ai_scheduler.py): recommends the best algorithm.
- [gui.py](gui.py): provides the Tkinter desktop interface.
- [charts.py](charts.py): draws the Gantt chart and comparison graphs.
- [utils.py](utils.py): saves and loads data.
- [data/sample_processes.json](data/sample_processes.json): example processes.
- [README.md](README.md): quick-start guide.

## 3. How to install the project

1. Install Python 3.10 or newer.
2. Open the project folder in VS Code.
3. Open a terminal inside the project folder.
4. Install Matplotlib:

```bash
pip install matplotlib
```

5. Run the application:

```bash
python main.py
```

## 4. How the application works

### Step 1: Add processes

Enter the number of processes, then fill the process table with:
- Process ID
- Arrival Time
- Burst Time
- Priority

### Step 2: Choose quantum

Set the quantum value for Round Robin.

### Step 3: Run the simulation

The system executes the scheduling algorithm and displays the results.

### Step 4: Compare and analyze

You can view:
- Gantt chart
- comparison graphs
- AI recommendation
- JSON export
- PDF export

## 5. Explanation of the scheduling algorithms

### FCFS
First Come First Serve executes processes in the order they arrive.

### SJF
Shortest Job First selects the smallest burst time first.

### SRTF
Shortest Remaining Time First is the preemptive version of SJF.

### Priority Scheduling
Processes with lower priority values are handled first.

### Round Robin
Each process receives a fixed time slice called the quantum.

## 6. Viva questions and answers

### Q1. What is CPU scheduling?
A1. CPU scheduling is the method used by the operating system to decide which process gets CPU time.

### Q2. Why is scheduling important?
A2. It improves CPU efficiency, reduces waiting time, and increases system responsiveness.

### Q3. What is the difference between preemptive and non-preemptive scheduling?
A3. Preemptive scheduling can interrupt a running process; non-preemptive scheduling cannot.

### Q4. What is the purpose of the Gantt chart?
A4. It visually shows the order and timing of process execution.

### Q5. What is the quantum in Round Robin?
A5. It is the fixed time slice given to each process in a round-robin cycle.

## 7. Possible interview questions

- What is the difference between FCFS and SJF?
- Why is Round Robin used in time-sharing systems?
- What are waiting time and turnaround time?
- What is the role of the AI recommendation system in this project?
- How would you improve this project further?

## 8. Common errors and solutions

### Error: Module not found: matplotlib
Solution: Run pip install matplotlib.

### Error: Python not recognized
Solution: Install Python and add it to PATH.

### Error: Tkinter window does not open
Solution: Make sure Python was installed with Tkinter support.

### Error: No processes loaded
Solution: Add processes manually or load the sample data.

## 9. Suggested screenshots

After running the project, you can take screenshots of:
- the main screen
- the process table
- the Gantt chart
- the comparison graph
- the AI recommendation message

These screenshots are useful for portfolio presentation and project demonstration.
