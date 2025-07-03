import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def find_newest_csv_files(count=2):
    script_directory = Path(__file__).parent

    # Look for files that contain 'csv' in the name
    csv_files = [
        file_path for file_path in script_directory.iterdir()
        if file_path.is_file() and 'csv' in file_path.name.lower()
    ]

    if not csv_files:
        print("No CSV-like files found in this folder.")
        return []

    sorted_files = sorted(csv_files, key=lambda f: f.stat().st_mtime, reverse=True)
    newest = sorted_files[:count]

    print("Newest CSV files:")
    for f in newest:
        print(f" - {f.name} (Last Modified: {f.stat().st_mtime})")

    return newest

def analyze_csv(file_path):
    df = pd.read_csv(file_path, on_bad_lines='skip')  # pandas >= 1.3.0

    df_numeric = df.select_dtypes(include='number')

    if df_numeric.empty:
        print(f"Skipping {file_path.name} (no numeric columns found).")
        return

    stats = pd.DataFrame({
        'Mean': df_numeric.mean(),
        'Median': df_numeric.median(),
        'P90': df_numeric.quantile(0.9)
    })

    print(f"\nStatistics for {file_path.name}:\n")
    print(stats)

    # Save table as image
    fig, ax = plt.subplots(figsize=(10, len(stats) * 0.5 + 1))
    ax.axis('off')
    table = ax.table(
        cellText=stats.round(2).values,
        colLabels=stats.columns,
        rowLabels=stats.index,
        loc='center',
        cellLoc='center'
    )
    table.scale(1, 1.5)
    plt.tight_layout()

    output_path = file_path.with_name(file_path.stem + '_stats.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path.name}")

def main():
    newest_files = find_newest_csv_files()
    for file_path in newest_files:
        analyze_csv(file_path)

if __name__ == "__main__":
    main()
