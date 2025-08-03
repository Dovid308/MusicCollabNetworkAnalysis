import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Last.fm API credentials from .env file
API_KEY = os.getenv("LAST_FM")

# Define the base URL for the Last.fm API
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

class GenreMapper:
    def __init__(self):
        self.genre_mapping = {
            # --- POP ---
            "pop": "pop",
            "dance pop": "pop",
            "electropop": "pop",
            "synthpop": "pop",
            "hyperpop": "pop",
            "bedroom pop": "pop",
            "teen pop": "pop",
            "art pop": "pop",
            "pop rock": "pop",
            "power pop": "pop",
            "indie pop": "pop",
            "kpop": "pop",
            "k-pop": "pop",
            "jpop": "pop",
            "j-pop": "pop",

            # --- HIP HOP / RAP ---
            "rap": "hip hop",
            "trap": "hip hop",
            "hip hop": "hip hop",
            "hiphop": "hip hop",
            "hip-hop": "hip hop",
            "boom bap": "hip hop",
            "drill": "hip hop",
            "gangsta rap": "hip hop",
            "conscious rap": "hip hop",
            "alternative hip hop": "hip hop",
            "lofi hip hop": "hip hop",
            "lo-fi hip hop": "hip hop",
            "mumble rap": "hip hop",
            "cloud rap": "hip hop",
            "grime": "hip hop",
            "g-funk": "hip hop",
            "chopped and screwed": "hip hop",
            "east coast hip hop": "hip hop",
            "west coast hip hop": "hip hop",
            "dirty south rap": "hip hop",
            "crunk": "hip hop",

            # --- LATIN ---
            "reggaeton": "latin",
            "latin trap": "latin",
            "urbano": "latin",
            "latin pop": "latin",
            "regional mexican": "latin",
            "banda": "latin",
            "cumbia": "latin",
            "bachata": "latin",
            "salsa": "latin",
            "merengue": "latin",
            "vallenato": "latin",
            "mariachi": "latin",

            # --- ROCK ---
            "rock": "rock",
            "classic rock": "rock",
            "alternative rock": "rock",
            "indie rock": "rock",
            "garage rock": "rock",
            "psych rock": "rock",
            "psychedelic rock": "rock",
            "math rock": "rock",
            "grunge": "rock",
            "stoner rock": "rock",
            "progressive rock": "rock",
            "prog rock": "rock",
            "folk rock": "rock",
            "blues rock": "rock",
            "industrial rock": "rock",
            "soft rock": "rock",
            "gothic rock": "rock",
            "glam rock": "rock",
            "post-rock": "rock",

            # --- METAL (split from Rock) ---
            "metal": "metal",
            "heavy metal": "metal",
            "thrash metal": "metal",
            "black metal": "metal",
            "death metal": "metal",
            "doom metal": "metal",
            "power metal": "metal",
            "nu metal": "metal",
            "groove metal": "metal",
            "folk metal": "metal",
            "viking metal": "metal",
            "progressive metal": "metal",
            "prog metal": "metal",
            "post-metal": "metal",
            "sludge metal": "metal",
            "symphonic metal": "metal",
            "deathcore": "metal",
            "metalcore": "metal",

            # --- PUNK (split from Rock) ---
            "punk": "punk",
            "punk rock": "punk",
            "post-punk": "punk",
            "hardcore punk": "punk",
            "ska punk": "punk",
            "emo": "punk",
            "screamo": "punk",
            "crust punk": "punk",
            "anarcho punk": "punk",
            "pop punk": "punk",

            # --- EDM / ELECTRONIC ---
            "edm": "electronic",
            "electronic": "electronic",
            "electronica": "electronic",
            "house": "electronic",
            "tech house": "electronic",
            "deep house": "electronic",
            "progressive house": "electronic",
            "future house": "electronic",
            "bass house": "electronic",
            "tropical house": "electronic",
            "trance": "electronic",
            "psytrance": "electronic",
            "dubstep": "electronic",
            "brostep": "electronic",
            "future bass": "electronic",
            "drum and bass": "electronic",
            "dnb": "electronic",
            "jungle": "electronic",
            "breakbeat": "electronic",
            "electro house": "electronic",
            "glitch hop": "electronic",
            "chillwave": "electronic",
            "vaporwave": "electronic",
            "synthwave": "electronic",
            "ambient electronic": "electronic",
            "idm": "electronic",

            # --- R&B / SOUL ---
            "r&b": "r&b",
            "rnb": "r&b",
            "soul": "r&b",
            "neo soul": "r&b",
            "alt r&b": "r&b",
            "contemporary r&b": "r&b",
            "funk": "r&b",
            "new jack swing": "r&b",
            "quiet storm": "r&b",

            # --- COUNTRY ---
            "country": "country",
            "alt country": "country",
            "country pop": "country",
            "outlaw country": "country",
            "bluegrass": "country",
            "americana": "country",

            # --- REGGAE ---
            "reggae": "reggae",
            "dancehall": "reggae",
            "ska": "reggae",
            "roots reggae": "reggae",
            "dub": "reggae",
            "rocksteady": "reggae",

            # --- CLASSICAL ---
            "classical": "classical",
            "baroque": "classical",
            "romantic era": "classical",
            "modern classical": "classical",
            "opera": "classical",
            "chamber music": "classical",
            "symphony": "classical",
            "contemporary classical": "classical",

            # --- OTHER / MISC ---
            "jazz": "other",
            "fusion": "other",
            "world": "other",
            "afrobeat": "other",
            "blues": "other",
            "folk": "other",
            "new age": "other",
            "soundtrack": "other",
            "anime music": "other",
            "video game music": "other",
            "musical theatre": "other",
            "ambient": "other",
            "spoken word": "other",
            "comedy": "other",
            "children's music": "other",
            "holiday": "other",
            "christmas music": "other",
        }

    def normalize_first_genre(self, tags):
        """
        Normalize the first recognized genre from a list of tags.
        If no known genres are found, return 'unknown'.

        Args:
            tags (list): List of tag strings

        Returns:
            str: Single normalized genre
        """
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower in self.genre_mapping:
                return self.genre_mapping[tag_lower]
        return "unknown"


def get_top_artists(total_artists=100):
    """Fetches top artists from Last.fm"""
    artists = []
    seen_ids = set()
    per_page = 50
    total_pages = (total_artists + per_page - 1) // per_page  # number of pages needed

    for page in range(1, total_pages + 1):
        params = {
            'method': 'chart.gettopartists',
            'api_key': API_KEY,
            'format': 'json',
            'limit': per_page,
            'page': page
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            top_artists = data.get('artists', {}).get('artist', [])
            for artist in top_artists:
                mbid = artist.get('mbid')
                url = artist.get('url')
                unique_id = mbid if mbid else url  # use mbid if available, otherwise url

                if unique_id not in seen_ids:
                    seen_ids.add(unique_id)
                    artists.append({
                        "name": artist['name'],
                        "listeners": artist['listeners'],
                        "mbid": mbid,
                        "url": url
                    })
        else:
            print(f"Error: Unable to retrieve artists. Status code {response.status_code}")
    return artists


def get_artist_tags(artist_name):
    """Fetches the top tags for a given artist"""
    params = {
        'method': 'artist.gettoptags',
        'artist': artist_name,
        'api_key': API_KEY,
        'format': 'json'
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        tags = data.get('toptags', {}).get('tag', [])
        # Return top 5 tags (or fewer if not available)
        top_tags = [tag['name'] for tag in tags[:5]]  # You can adjust number of tags here
        return top_tags
    else:
        print(f"Warning: Unable to fetch tags for {artist_name}. Status code {response.status_code}")
        return []


def save_to_json(artists, filename="data/artists_with_normalized_genres.json"):
    """Saves artist data to a JSON file"""
    output_dir = os.path.dirname(filename)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(artists, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {filename}")


def main(num_artists=100, output_file="data/artists_with_normalized_genres.json"):
    """
    Main function to fetch artist data, enrich with tags, normalize genres, and save to JSON
    """
    print(f"Fetching top {num_artists} artists from Last.fm...")
    top_artists = get_top_artists(total_artists=num_artists)
    
    if not top_artists:
        print("No artists data found. Exiting.")
        return
    
    mapper = GenreMapper()
    enriched_artists = []
    
    print(f"Processing {len(top_artists)} artists...")
    for i, artist in enumerate(top_artists):
        if i % 10 == 0 and i > 0:
            print(f"Processed {i}/{len(top_artists)} artists")
            
        name = artist["name"]
        listeners = artist["listeners"]
        
        # Get tags for this artist
        tags = get_artist_tags(name)
        
        # Normalize the genre based on tags
        normalized_genre = mapper.normalize_first_genre(tags)
        
        # Create enriched artist object
        enriched_artists.append({
            "name": name,
            "listeners": listeners,
            "normalized_genre": normalized_genre
        })
    
    # Save combined data to JSON
    save_to_json(enriched_artists, output_file)
    print(f"Successfully processed {len(enriched_artists)} artists with normalized genres")


if __name__ == "__main__":
    # Set the number of artists to fetch (default is 100)
    NUM_ARTISTS = 2000  # You can change this value
    OUTPUT_FILE = "data/artists_with_normalized_genres.json"
    
    main(num_artists=NUM_ARTISTS, output_file=OUTPUT_FILE)