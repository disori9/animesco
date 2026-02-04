import requests

def get_anilist_data(anime_title):
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

		media_list = data["data"]["Page"]["media"]
		
		if not media_list:
			raise ValueError(f"No results found for {anime_title}")
		
		anime_results = media_list[0]
		anime_data = anime_results
   
		return anime_data

	else:
		raise ConnectionError("Cannot connect to the database")

def get_anilist_score(anime_title):
    anime_data = get_anilist_data(anime_title)
    anilist_score = anime_data.get("averageScore") / 10.0
    return anilist_score