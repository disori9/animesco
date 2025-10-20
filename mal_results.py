import requests


base_url = "https://api.jikan.moe/v4/anime"
# anime_title = input("Please input your title, accurate title produces accurate results: ")
anime_title = "Attack on Titan"
# q is basically the anime title, while limit limits the search results based on the integer given, default is 25
# We need to create a params object to use the optional argument for requests' query parameters
params = {
    "q": anime_title,
    "limit": 5
}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    
    anime_info = response.json()
    print("/n--- Search Results ---")
    
    if not anime_info.get("data"):
        print(f"No results found for '{anime_title}'. Exiting.")
    else:
        # The problem was basically how do I make sure that when the user searches for a show with an incomplete name, they'll get the result they want
        # The solution was to show the user the top 5 results with their corresponding index and then ask the user for what show they want, getting the index from them
        # Then getting the data from that index to have a variable which holds the show's data
        for index, anime in enumerate(anime_info["data"]):
            print(f"Anime [{index}]: {anime["title"]} (MAL ID: {anime["mal_id"]})")
        while True:
            try:
                anime_selected = int(input("\nPlease input the number of the title you want: "))
                anime_data = anime_info["data"][anime_selected]
                break
            except (ValueError, IndexError):
                print("Invalid input. Please enter one of the numbers listed.")
        
        # .get basically gets the data from a key 
        mal_score = anime_data.get("score")
        mal_id = anime_data.get("mal_id")
        
        print("\n--- MyAnimeList Data ---")
        print(f"Selected Anime: {anime_data["title"]}")
        print(f"MAL Score: {mal_score}")
        print(f"Unique MAL ID: {mal_id}")
        
else:
    print(f"Request failed with status code: {response.status_code}")
    