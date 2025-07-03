import csv
import statistics
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def process_csv_files(filenames, treeview):
    treeview.delete(*treeview.get_children())  # Clear the table

    for filename in filenames:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row

            # Initialize a dictionary to store the column statistics
            column_stats = {column: [] for column in header}

            # Read each row and append values to the corresponding column
            for row in reader:
                for i, value in enumerate(row):
                    column = header[i]
                    try:
                        column_stats[column].append(float(value))
                    except ValueError:
                        pass

            # Calculate statistics for each column
            file_stats = []
            for column in header:
                if column_stats[column]:
                    mean = statistics.mean(column_stats[column])
                    p50 = statistics.median(column_stats[column])
                    p90 = statistics.quantiles(column_stats[column], n=11)[9]
                    file_stats.append([mean, p50, p90])
                else:
                    file_stats.append(["-", "-", "-"])

            # Insert statistics into the table
            file_stats = list(zip(*file_stats))  # Transpose the stats
            file_stats.insert(0, ["Mean", "P50 (Median)", "P90"])  # Add percentile headers
            treeview.insert("", "end", text=filename, values=file_stats)

def open_file_dialog(treeview):
    filenames = filedialog.askopenfilenames(title="Select .csv files", filetypes=[("CSV Files", "*.csv")])
    process_csv_files(filenames, treeview)
    messagebox.showinfo("Processing Complete", "CSV files processed successfully!")

# Create the main window
window = tk.Tk()
window.title("CSV Viewer")

# Create a button for file selection
button = tk.Button(window, text="Select .csv files", command=lambda: open_file_dialog(treeview))
button.pack(pady=20)

# Create a Treeview widget for displaying the statistics in a table
treeview = ttk.Treeview(window, columns=("Metric", "Mean", "P50 (Median)", "P90"), show="headings")
treeview.heading("Metric", text="Metric")
treeview.heading("Mean", text="Mean")
treeview.heading("P50 (Median)", text="P50 (Median)")
treeview.heading("P90", text="P90")
treeview.pack(padx=10, pady=10)

# Set column widths
treeview.column("Metric", width=150, anchor="center")
treeview.column("Mean", width=100, anchor="center")
treeview.column("P50 (Median)", width=100, anchor="center")
treeview.column("P90", width=100, anchor="center")

# Run the main event loop
window.mainloop()
