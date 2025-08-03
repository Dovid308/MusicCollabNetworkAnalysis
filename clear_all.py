import os
import shutil

def empty_folders(folder_paths):
    for folder in folder_paths:
        if os.path.isdir(folder):
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    print(f"Deleted: {item_path}")
                except Exception as e:
                    print(f"Failed to delete {item_path}. Reason: {e}")
        else:
            print(f"Not a directory or doesn't exist: {folder}")

# Example usage:
folders_to_empty = [
    'data',
    'graph_genre',
    'graph_labels',
    'analysis/analysis_results'
]

empty_folders(folders_to_empty)
