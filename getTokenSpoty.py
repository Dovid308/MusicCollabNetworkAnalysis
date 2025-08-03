import requests
import os
from dotenv import load_dotenv, set_key

# Load environment variables
load_dotenv()

# Spotify API credentials from .env file
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Function to get access token from Spotify API
def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(auth_url, data=auth_data)
    response_data = response.json()

    # Check if the request was successful
    if response.status_code == 200:
        access_token = response_data.get("access_token")
        return access_token
    else:
        print("Failed to get access token:", response_data)
        return None

# Save the access token to .env file
def save_token_to_env(token):
    if token:
        # Load the .env file
        load_dotenv()

        # Save the token in the .env file
        set_key(".env", "ACCESS_TOKEN", token)
        print("Access token saved to .env")
    else:
        print("No token to save.")

# Main function to get and save the token
if __name__ == "__main__":
    token = get_access_token()
    save_token_to_env(token)
