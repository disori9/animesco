import requests

def get_mal_data(anime_title):

	base_url = "https://api.jikan.moe/v4/anime"
	# anime_title = input("Please input your title, accurate title produces accurate results: ")
	# q is basically the anime title, while limit limits the search results based on the integer given, default is 25
	# We need to create a params object to use the optional argument for requests' query parameters
	params = {
		"q": anime_title,
		"limit": 1
	}

	response = requests.get(base_url, params=params)

	if response.status_code == 200:
		
		animes_found = response.json()
		
		if not animes_found.get("data"):
			print(f"No results found for '{anime_title}'. Exiting.")
		else:
			anime_data = animes_found["data"][0]

		return anime_data
			
	else:
		print(f"Request failed with status code: {response.status_code}")
		return None

def get_mal_score(anime_title):
	anime_data = get_mal_data(anime_title)
	mal_score = anime_data.get("score")
	return mal_score

	# .get basically gets the data from a key 
	# mal_score = anime_data.get("score")
	# mal_id = anime_data.get("mal_id")

	# print("\n--- MyAnimeList Data ---")
	# print(f"Selected Anime: {anime_data["title"]}")
	# print(f"MAL Score: {mal_score}")
	# print(f"Unique MAL ID: {mal_id}")