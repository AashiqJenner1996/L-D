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

            # Initialize a list to store the column statistics
            column_stats = [[] for _ in range(len(header))]

            # Read each row and append values to the corresponding column
            for row in reader:
                for i, value in enumerate(row):
                    try:
                        column_stats[i].append(float(value))
                    except ValueError:
                        pass

            # Calculate statistics for each column
            file_stats = []
            for i, column in enumerate(header):
                if column_stats[i]:
                    mean = statistics.mean(column_stats[i])
                    p50 = statistics.median(column_stats[i])
                    p90 = statistics.quantiles(column_stats[i], n=11)[9]
                    file_stats.append([column, mean, p50, p90])
                else:
                    file_stats.append([column, "-", "-", "-"])

            # Insert statistics into the table
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
treeview = ttk.Treeview(window, columns=("Column", "Mean", "P50 (Median)", "P90"))
treeview.heading("#0", text="File")
treeview.heading("Column", text="Column")
treeview.heading("Mean", text="Mean")
treeview.heading("P50 (Median)", text="P50 (Median)")
treeview.heading("P90", text="P90")
treeview.pack(padx=10, pady=10)

# Run the main event loop
window.mainloop()
