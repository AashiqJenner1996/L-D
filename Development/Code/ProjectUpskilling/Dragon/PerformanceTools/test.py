from pathlib import Path

directory = Path(__file__).parent  # or Path.cwd() if you prefer

print(f"Contents of {directory}:\n")

for item in directory.iterdir():
    item_type = "File" if item.is_file() else "Folder"
    print(f"{item_type:8} - {item.name}")
