import requests

# First of all we need the query to be sent to post
# In the query parameters, you need to set the variables you define inside the fields first. So $search in media has a corresponding $search: String! in the query parameters
# Their value is their type.
query = '''
query ($search: String!, $perPage: Int) {
  Page (perPage: $perPage) {
    media(search: $search, type: ANIME) {
      id
      title {
        english
      }
      averageScore
    }
  }
}
'''

# And then for the variables that we created in the query (see names with $ on them), we need to create the corresp. variables
anime_title = 'Overlord'

variables = {
    'search': anime_title,
    'perPage': 5
}

# Get the base url that we send the post request unto
base_url = 'https://graphql.anilist.co'


 # Make the request

response = requests.post(base_url, json={'query': query, 'variables': variables}) 

if response.status_code == 200:
    data = response.json()
    print("/n--- Search Results ---")
    
    if not data.get("data"):
        print(f"No results found for '{anime_title}'. Exiting.")
    else:
        anime_results = data["data"]["Page"]["media"]
        
        for index, anime in enumerate(anime_results):
            print(f"Anime [{index}]: {anime["title"]["english"]}")
        
        while True:
            try:
                anime_selected = int(input("\nPlease input the number of the title you want: "))
                anime_data = anime_results[anime_selected]
                break
            except(ValueError, IndexError):
                print("Invalid input. Please enter the number beside Anime[#]")
        
        anilist_score = anime_data.get("averageScore") / 10.0
        anilist_id = anime_data.get("id")
        anilist_title = anime_data.get("title").get("english")
        
        print("\n--- AniList Data ---")
        print(f"Selected Anime: {anilist_title}")
        print(f"AniList Score: {anilist_score}")
        print(f"Unique AniList ID: {anilist_id}")

else:
    print(f"Request failed with status code: {response.status_code}")