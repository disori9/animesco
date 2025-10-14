import requests


base_url = "https://api.jikan.moe/v4/anime"

params = {
    "q": "Attack on Titan",
    "limit": 1
}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    print("Data retrieved")
    anime_info = response.json()
else:
    print(f"Request failed with status code: {response.status_code}")
    
print(anime_info["data"])