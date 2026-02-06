import requests

def get_verified_title():
	search_anime = input("What show do you want to search? ")
	base_url = "https://api.jikan.moe/v4/anime"
	# anime_title = input("Please input your title, accurate title produces accurate results: ")
	# q is basically the anime title, while limit limits the search results based on the integer given, default is 25
	# We need to create a params object to use the optional argument for requests' query parameters
	params = {
		"q": search_anime,
		"limit": 5
	}

	response = requests.get(base_url, params=params)

	if response.status_code == 200:
		
		animes_found = response.json()
		
	# The problem was basically how do I make sure that when the user searches for a show with an incomplete name, they'll get the result they want
	# The solution was to show the user the top 5 results with their corresponding index and then ask the user for what show they want, getting the index from them
	# Then getting the data from that index to have a variable which holds the show's data
		print("\n--- Search Results ---")
		for index, anime in enumerate(animes_found["data"]):
			print(f"Anime [{index}]: {anime["title"]} (MAL ID: {anime["mal_id"]})")
		while True:
			try:
				anime_selected = int(input("\nPlease input the number of the title you want: "))
				anime_title = animes_found["data"][anime_selected]['title']
				break
			except (ValueError, IndexError):
				print("Invalid input. Please enter one of the numbers listed.")		
	else:
		print(f"Request failed with status code: {response.status_code}")
		return None

	return anime_title

def top_search_results(query):
	base_url = "https://api.jikan.moe/v4/anime"

	params = {
		"q": query,
		"limit": 5
	}

	response = requests.get(base_url, params=params)

	if response.status_code == 200:
		
		animes_found = response.json()
		candidates = []

		for anime in animes_found["data"]:
			anime_data = {'mal_id': anime['mal_id'], 'title': anime['title'], 'cover': anime["images"]["jpg"]["image_url"], 'synopsis': anime["synopsis"]}
			candidates.append(anime_data)
	else:
		print(f"Request failed with status code: {response.status_code}")
		return None

	return candidates
