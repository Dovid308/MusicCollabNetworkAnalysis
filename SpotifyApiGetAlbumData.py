import requests
import time
import os
import json
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

BASE_URL = "https://api.spotify.com/v1/"
MIN_DELAY = 1  # Min request delay
MAX_DELAY = 1.5  # Max request delay

def respectful_request(url, headers):
    """Handles rate limits and delays requests"""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(delay)
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 30))
        if retry_after > 300:  # If bigger than 5 minutes, exit
            print(f"Rate limit is too long: {retry_after} seconds. Exit.")
            exit()
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after + 1)
        return respectful_request(url, headers)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
    return response

def search_artist_id(artist_name):
    """
    Step 1: Search for artist to get ID (no need to fetch genres since they are already provided)
    Returns: artist_id
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    url = f"{BASE_URL}search?q={artist_name}&type=artist&limit=1"
    response = respectful_request(url, headers)
    
    if not response:
        print(f"Failed to find artist: {artist_name}")
        return None
    
    data = response.json()
    
    # Check if we have results
    if not data['artists']['items']:
        print(f"No results found for artist: {artist_name}")
        return None
    
    artist = data['artists']['items'][0]
    artist_id = artist['id']
    
    return artist_id

def get_latest_album(artist_id):
    """
    Step 2: Get the most recent album
    Returns: (album_name, album_id, release_date, label)
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    # Get up to 50 albums to ensure we have the latest
    url = f"{BASE_URL}artists/{artist_id}/albums?include_groups=album&limit=50"
    response = respectful_request(url, headers)
    
    if not response:
        print(f"Failed to get albums for artist ID: {artist_id}")
        return None, None, None, None
    
    data = response.json()
    
    if not data['items']:
        print(f"No albums found for artist ID: {artist_id}")
        return None, None, None, None
    
    # Sort albums by release date (newest first)
    albums = sorted(data['items'], key=lambda x: x['release_date'], reverse=True)
    latest_album = albums[0]
    
    album_name = latest_album['name']
    album_id = latest_album['id']
    release_date = latest_album['release_date']
    
    # Get additional album details including label
    album_url = f"{BASE_URL}albums/{album_id}"
    album_response = respectful_request(album_url, headers)
    
    if not album_response:
        print(f"Failed to get details for album ID: {album_id}")
        label = ""
    else:
        album_data = album_response.json()
        label = album_data.get('label', "")
    
    return album_name, album_id, release_date, label

def get_album_tracks(album_id, main_artist_id):
    """
    Step 3: Get tracks and extract featured artists
    Returns: list of featured artist names
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    url = f"{BASE_URL}albums/{album_id}/tracks?limit=50"
    response = respectful_request(url, headers)
    
    if not response:
        print(f"Failed to get tracks for album ID: {album_id}")
        return []
    
    data = response.json()
    feat_artists = set()  # Use set to avoid duplicates
    
    for track in data['items']:
        # Get all artists other than the main artist
        for artist in track['artists']:
            if artist['id'] != main_artist_id:
                feat_artists.add(artist['name'])
    
    return list(feat_artists)

def build_artist_summary(artist_name, artist_genre):
    """
    Step 4: Central wrapper function to build the final JSON
    """
    # Step 1: Get artist ID
    artist_id = search_artist_id(artist_name)
    if not artist_id:
        return None
    
    # Step 2: Get latest album info
    album, album_id, date_of_publication, label = get_latest_album(artist_id)
    if not album:
        return None
    
    # Step 3: Get featured artists
    feat = get_album_tracks(album_id, artist_id)
    
    # Build final JSON structure
    artist_data = {
        "album": album,
        "album_id": album_id,
        "artist_id": artist_id,
        "artist": artist_name,
        "artist_genre": artist_genre,  # Use the genre provided in the input JSON
        "label": label,
        "date_of_publication": date_of_publication,
        "feat": feat
    }
    
    return artist_data

def load_existing_data(output_file):
    """Load existing data from output file if it exists"""
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error reading {output_file}. File might be corrupted.")
            return []
    return []

def save_data(data, output_file):
    """Save data to output file"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {output_file}")

def main():
    input_file = "data/artists_with_normalized_genres.json"
    output_file = "data/latest_albums_details.json"

    if not ACCESS_TOKEN:
        print("No Spotify access token found. Set ACCESS_TOKEN in your .env.")
        return

    # Load input data
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_artists = json.load(f)
        print(f"Loaded {len(input_artists)} artists from {input_file}")
    except Exception as e:
        print(f"Failed to load artist file: {e}")
        return

    # Load existing output data
    existing_data = load_existing_data(output_file)
    print(f"Found {len(existing_data)} artists already processed in {output_file}")

    # Create dictionary of existing artists for quick lookup
    existing_artists = {entry["artist"]: True for entry in existing_data}
    
    # Find artists that need to be processed
    artists_to_process = [artist for artist in input_artists if artist["name"] not in existing_artists]
    print(f"Found {len(artists_to_process)} artists that need processing")

    # Process one by one
    for i, artist_entry in enumerate(artists_to_process):
        artist_name = artist_entry["name"]
        artist_genre = artist_entry["normalized_genre"]
        
        print(f"Processing {i+1}/{len(artists_to_process)}: {artist_name}")
        
        artist_data = build_artist_summary(artist_name, artist_genre)
        if artist_data:
            # Include original listener count
            artist_data["listeners"] = artist_entry.get("listeners", "")
            
            # Add to existing data
            existing_data.append(artist_data)
            
            # Save after each successful processing
            save_data(existing_data, output_file)
            print(f"Added {artist_name} to output file")
        else:
            print(f"Failed to process {artist_name}")
        
        # Optional: Save progress to a different file periodically
        if (i + 1) % 10 == 0:
            save_data(existing_data, "data/latest_albums_details_backup.json")
            print(f"Backup saved after processing {i+1} artists")

    print(f"\nAll done! Processed {len(artists_to_process)} new artists.")
    print(f"Total artists in output: {len(existing_data)}")

if __name__ == "__main__":
    main()