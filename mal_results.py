import requests

def search_results(animes_found):
	# The problem was basically how do I make sure that when the user searches for a show with an incomplete name, they'll get the result they want
	# The solution was to show the user the top 5 results with their corresponding index and then ask the user for what show they want, getting the index from them
	# Then getting the data from that index to have a variable which holds the show's data
	print("/n--- Search Results ---")
	for index, anime in enumerate(animes_found["data"]):
		print(f"Anime [{index}]: {anime["title"]} (MAL ID: {anime["mal_id"]})")
	while True:
		try:
			anime_selected = int(input("\nPlease input the number of the title you want: "))
			anime_data = animes_found["data"][anime_selected]
			break
		except (ValueError, IndexError):
			print("Invalid input. Please enter one of the numbers listed.")
	
	return anime_data

def get_mal_data(anime_title):

	base_url = "https://api.jikan.moe/v4/anime"
	# anime_title = input("Please input your title, accurate title produces accurate results: ")
	# q is basically the anime title, while limit limits the search results based on the integer given, default is 25
	# We need to create a params object to use the optional argument for requests' query parameters
	params = {
		"q": anime_title,
		"limit": 5
	}

	response = requests.get(base_url, params=params)

	if response.status_code == 200:
		
		animes_found = response.json()
		
		if not animes_found.get("data"):
			print(f"No results found for '{anime_title}'. Exiting.")
		else:
			anime_data = search_results(animes_found)

		return anime_data
			
	else:
		print(f"Request failed with status code: {response.status_code}")
		return None

def get_mal_score(anime_title):
	anime_data = get_mal_data(anime_title)
	mal_score = anime_data.get("score")
	return mal_score


score = get_mal_score("Overlord")
print(score)

	# .get basically gets the data from a key 
	# mal_score = anime_data.get("score")
	# mal_id = anime_data.get("mal_id")

	# print("\n--- MyAnimeList Data ---")
	# print(f"Selected Anime: {anime_data["title"]}")
	# print(f"MAL Score: {mal_score}")
	# print(f"Unique MAL ID: {mal_id}")