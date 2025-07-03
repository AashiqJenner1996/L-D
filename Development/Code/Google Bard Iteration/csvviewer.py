import csv
import statistics
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

def process_csv_files(filenames, output_text):
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

            # Calculate and display statistics for each column
            output_text.insert(tk.END, f"Statistics for file: {filename}\n")
            for i, column in enumerate(header):
                if column_stats[i]:
                    mean = statistics.mean(column_stats[i])
                    p50 = statistics.median(column_stats[i])
                    p90 = statistics.quantiles(column_stats[i], n=11)[9]
                    output_text.insert(tk.END, f"Column: {column}\n")
                    output_text.insert(tk.END, f"Mean: {mean}\n")
                    output_text.insert(tk.END, f"P50 (median): {p50}\n")
                    output_text.insert(tk.END, f"P90: {p90}\n")
                    output_text.insert(tk.END, "\n")
                else:
                    output_text.insert(tk.END, f"No numerical data found for column: {column}\n")
            output_text.insert(tk.END, "\n")

def open_file_dialog(output_text):
    filenames = filedialog.askopenfilenames(title="Select .csv files", filetypes=[("CSV Files", "*.csv")])
    process_csv_files(filenames, output_text)
    messagebox.showinfo("Processing Complete", "CSV files processed successfully!")

# Create the main window
window = tk.Tk()
window.title("CSV Viewer")

# Create a button for file selection
button = tk.Button(window, text="Select .csv files", command=lambda: open_file_dialog(output_text))
button.pack(pady=20)

# Create a text area for displaying the results
output_text = ScrolledText(window, height=100, width=400)
output_text.pack(padx=10, pady=10)

# Run the main event loop
window.mainloop()