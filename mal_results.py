import requests

def make_api_request(anime_title):

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
			raise ValueError(f"No results found for {anime_title}")
		
		anime_data = animes_found["data"][0]

		return anime_data
			
	else:
		raise ConnectionError("Cannot connect to the database")

def get_mal_data(anime_title):
	mal_data = make_api_request(anime_title)

	return mal_data