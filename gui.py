from utils import export_to_pdf, load_sample_data, save_results_json
from scheduler import compare_algorithms, run_selected_algorithm
from process import Process
from charts import draw_comparison_graph, draw_gantt_chart
from algorithms import fcfs, priority_scheduling, round_robin, sjf_non_preemptive, srtf
from ai_scheduler import recommend_best_algorithm
import json
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

import matplotlib
matplotlib.use("TkAgg")


class SmartCPUSchedulerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Smart CPU Scheduler")
        self.root.geometry("1200x780")
        self.root.configure(bg="#0f172a")

        self.processes: List[Process] = []
        self.results: dict = {}
        self.build_ui()

    def build_ui(self) -> None:
        title = ttk.Label(self.root, text="Smart CPU Scheduler", font=(
            "Segoe UI", 24, "bold"), foreground="#38bdf8")
        title.pack(pady=(20, 5))

        subtitle = ttk.Label(
            self.root, text="AI-powered CPU scheduling simulator", foreground="#cbd5e1")
        subtitle.pack(pady=(0, 15))

        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(top_frame, text="Number of Processes", foreground="#e2e8f0").grid(
            row=0, column=0, padx=5, pady=5)
        self.process_count_var = tk.StringVar(value="4")
        ttk.Entry(top_frame, textvariable=self.process_count_var,
                  width=10).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top_frame, text="Quantum", foreground="#e2e8f0").grid(
            row=0, column=2, padx=5, pady=5)
        self.quantum_var = tk.StringVar(value="2")
        ttk.Entry(top_frame, textvariable=self.quantum_var,
                  width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(top_frame, text="Algorithm", foreground="#e2e8f0").grid(
            row=0, column=4, padx=5, pady=5)
        self.algorithm_var = tk.StringVar(value="FCFS")
        ttk.Combobox(top_frame, textvariable=self.algorithm_var, values=[
            "FCFS", "SJF", "SRTF", "Priority Scheduling", "Round Robin", "Compare All"], width=18, state="readonly").grid(row=0, column=5, padx=5, pady=5)

        self.add_button = ttk.Button(
            top_frame, text="Add Process", command=self.add_process_row)
        self.add_button.grid(row=0, column=6, padx=8)

        self.load_button = ttk.Button(
            top_frame, text="Load Sample Data", command=self.load_sample_data)
        self.load_button.grid(row=0, column=7, padx=8)

        self.run_button = ttk.Button(
            top_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=0, column=8, padx=8)

        self.reset_button = ttk.Button(
            top_frame, text="Reset", command=self.reset_data)
        self.reset_button.grid(row=0, column=9, padx=8)

        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=(
            "pid", "arrival", "burst", "priority"), show="headings")
        self.tree.heading("pid", text="Process ID")
        self.tree.heading("arrival", text="Arrival Time")
        self.tree.heading("burst", text="Burst Time")
        self.tree.heading("priority", text="Priority")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)

        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(buttons_frame, text="Show Gantt Chart",
                   command=self.show_gantt).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Compare Algorithms",
                   command=self.show_comparison).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="AI Recommendation",
                   command=self.show_ai_recommendation).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Save JSON",
                   command=self.save_json).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Export PDF",
                   command=self.export_pdf).pack(side="left", padx=5)

        self.result_text = tk.Text(
            self.root, height=12, bg="#111827", fg="#f9fafb")
        self.result_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.edit_entry: tk.Entry | None = None
        self.edit_item = None
        self.edit_column = None
        self.add_process_row()

    def add_process_row(self) -> None:
        try:
            count = int(self.process_count_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid input", "Please enter a valid number of processes")
            return

        self.tree.delete(*self.tree.get_children())
        self.processes = []
        for idx in range(count):
            process = Process(pid=f"P{idx + 1}",
                              arrival_time=0, burst_time=0, priority=0)
            self.processes.append(process)
            self.tree.insert("", "end", values=(
                process.pid, "", "", ""))

    def load_sample_data(self) -> None:
        self.processes = load_sample_data()
        self.tree.delete(*self.tree.get_children())
        for process in self.processes:
            self.tree.insert("", "end", values=(
                process.pid, process.arrival_time, process.burst_time, process.priority))
        messagebox.showinfo("Loaded", "Sample data has been loaded")

    def reset_data(self) -> None:
        self.processes = []
        self.results = {}
        self.tree.delete(*self.tree.get_children())
        self.result_text.delete("1.0", tk.END)
        self.process_count_var.set("4")
        self.quantum_var.set("2")
        self.algorithm_var.set("FCFS")
        messagebox.showinfo("Reset", "All data has been cleared")

    def run_simulation(self) -> None:
        try:
            quantum = float(self.quantum_var.get())
        except ValueError:
            messagebox.showerror("Invalid quantum", "Quantum must be a number")
            return

        self.processes = []
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            if len(values) < 4:
                continue
            try:
                arrival_time = float(values[1])
                burst_time = float(values[2])
                priority = int(values[3])
            except (ValueError, TypeError):
                messagebox.showerror(
                    "Invalid process data",
                    "Please enter valid numeric values for arrival time, burst time, and priority"
                )
                return

            self.processes.append(
                Process(
                    pid=str(values[0]),
                    arrival_time=arrival_time,
                    burst_time=burst_time,
                    priority=priority,
                )
            )

        if not self.processes:
            messagebox.showwarning(
                "No data", "Please add or load processes first")
            return

        algorithm = self.algorithm_var.get()
        self.results = run_selected_algorithm(
            self.processes, algorithm, quantum)
        self.display_results(self.results)

    def display_results(self, result: dict) -> None:
        self.result_text.delete("1.0", tk.END)
        if "comparison" in result:
            text = "Comparison Results\n\n"
            for name, details in result["comparison"].items():
                text += f"{name}: Avg Waiting={details['avg_waiting_time']}, Avg Turnaround={details['avg_turnaround_time']}, Avg Response={details['avg_response_time']}\n"
            self.result_text.insert(tk.END, text)
        else:
            text = f"Algorithm: {result.get('algorithm', 'N/A')}\n"
            text += f"Completion Time: {result.get('completion_time', 'N/A')}\n"
            text += f"Average Waiting Time: {result.get('avg_waiting_time', 'N/A')}\n"
            text += f"Average Turnaround Time: {result.get('avg_turnaround_time', 'N/A')}\n"
            text += f"Average Response Time: {result.get('avg_response_time', 'N/A')}\n"
            text += f"CPU Utilization: {result.get('cpu_utilization', 'N/A')}%\n"
            text += f"Throughput: {result.get('throughput', 'N/A')}\n"
            self.result_text.insert(tk.END, text)

    def show_gantt(self) -> None:
        if not self.results:
            messagebox.showwarning("No results", "Run the simulation first")
            return
        draw_gantt_chart(self.results)

    def show_comparison(self) -> None:
        if not self.processes:
            messagebox.showwarning("No data", "Add or load processes first")
            return
        self.results = compare_algorithms(
            self.processes, float(self.quantum_var.get()))
        self.display_results(self.results)
        draw_comparison_graph(self.results)

    def on_double_click(self, event: tk.Event) -> None:
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not row_id or column == "#1":
            return

        col_index = int(column.replace("#", "")) - 1
        bbox = self.tree.bbox(row_id, column)
        if not bbox:
            return

        self.edit_item = row_id
        self.edit_column = col_index
        x, y, width, height = bbox
        cell_value = self.tree.item(row_id, "values")[col_index]

        self.edit_entry = tk.Entry(self.tree)
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.insert(0, cell_value)
        self.edit_entry.focus()
        self.edit_entry.bind("<Return>", self.commit_edit)
        self.edit_entry.bind("<FocusOut>", self.commit_edit)

    def commit_edit(self, event: tk.Event) -> None:
        if not self.edit_entry or not self.edit_item or self.edit_column is None:
            return

        new_value = self.edit_entry.get().strip()
        self.edit_entry.destroy()
        self.edit_entry = None

        values = list(self.tree.item(self.edit_item, "values"))
        values[self.edit_column] = new_value
        self.tree.item(self.edit_item, values=values)
        self.edit_item = None
        self.edit_column = None

    def show_ai_recommendation(self) -> None:
        if not self.processes:
            messagebox.showwarning("No data", "Add or load processes first")
            return
        recommendation = recommend_best_algorithm(
            self.processes, float(self.quantum_var.get()))
        self.results = recommendation
        self.display_results(self.results)
        messagebox.showinfo("Recommendation", recommendation["reason"])

    def save_json(self) -> None:
        if not self.results:
            messagebox.showwarning(
                "No results", "Run or compare algorithms first")
            return
        path = "results.json"
        save_results_json(path, self.results)
        messagebox.showinfo("Saved", f"Results saved to {path}")

    def export_pdf(self) -> None:
        if not self.results:
            messagebox.showwarning(
                "No results", "Run or compare algorithms first")
            return
        path = "results.pdf"
        export_to_pdf(path, json.dumps(self.results, indent=2))
        messagebox.showinfo("Exported", f"Results exported to {path}")


def main() -> None:
    root = tk.Tk()
    app = SmartCPUSchedulerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
