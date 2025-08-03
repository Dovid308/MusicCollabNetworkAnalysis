# album_filter.py
import json
import os
from datetime import datetime

# Configuration
TARGET_GENRE = None  # Set to None if you don't want genre filtering
MIN_DATE = "2023-01-01"

# File paths
input_file = "data/latest_albums_details_labels_normalized.json"  # <-- use the updated normalized file
safe_genre = TARGET_GENRE.replace(" ", "_") if TARGET_GENRE else 'all_genres'
output_file = f"data/{safe_genre}_post_{MIN_DATE}_albums.json"

def is_after_min_date(date_str, min_date_str):
    """
    Check if a date string is after the minimum date.
    """
    try:
        pub_date = datetime.strptime(date_str, "%Y-%m-%d")
        min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
        return pub_date >= min_date
    except ValueError:
        return False

def main():
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found at {input_file}")

    # Read input JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filter and process
    filtered_albums = []
    for entry in data.get("data", []):  # Adjusted to access the 'data' list inside the JSON
        album = entry  # Each album is now an entry within 'data'
        artist_genre = album.get("artist_genre", "")  # Use 'artist_genre'
        pub_date = album.get("date_of_publication", "")

        # Check publication date
        if not is_after_min_date(pub_date, MIN_DATE):
            continue

        # If genre filtering is ON
        if TARGET_GENRE:
            if TARGET_GENRE.lower() in artist_genre.lower():  # Compare the genre, case-insensitive
                filtered_albums.append(album)
        else:
            # No genre filtering
            filtered_albums.append(album)

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save filtered data
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "total_entries": len(filtered_albums)
            },
            "data": filtered_albums
        }, f, indent=4, ensure_ascii=False)

    print(f"Filtered albums published after {MIN_DATE}: {len(filtered_albums)} results")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
