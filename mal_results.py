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

def get_anime_by_id(mal_id):
    """Fetches exact anime details from Jikan using the MAL ID."""
    base_url = f"https://api.jikan.moe/v4/anime/{mal_id}"
    
    response = requests.get(base_url)
    
    if response.status_code == 200:
        data = response.json()
        if not data.get("data"):
            raise ValueError(f"No results found for ID {mal_id}")
        
        # returns exactly one dictionary
        return data["data"] 
            
    else:
        raise ConnectionError("Cannot connect to the database")
	

def get_mal_recommendations(mal_id):
	base_url = f"https://api.jikan.moe/v4/anime/{mal_id}/recommendations"

	response = requests.get(base_url)

	if response.status_code == 200:
		data = response.json()
		if not data.get("data"):
			raise ValueError(f"No results found for ID {mal_id}")

		recommendations = []
		for rec in data["data"]:
			entry = rec["entry"]
			votes = rec["votes"]

			recommendation = {}
			recommendation["mal_id"] = entry["mal_id"]
			recommendation["title"] = entry["title"]
			recommendation["cover"] = entry["images"]["jpg"]["image_url"]
			recommendation['votes'] = votes
			recommendations.append(recommendation)

		return recommendations
	else:
		raise ConnectionError("Cannot connect to the database")
	


if __name__ == "__main__":
    # This block only runs if you execute THIS file directly.
    # It won't run when app.py imports it.
    
    print("Testing Jikan Recommendations...")
    try:
        # Let's test with ID 37430 (That Time I Got Reincarnated as a Slime)
        test_data = get_mal_recommendations(37430)
        
        for item in test_data:
            print(f"Title: {item['title']}, Votes: {item['votes']}")
            
    except Exception as e:
        print(f"Error: {e}")