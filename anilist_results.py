import requests

def get_anilist_data(mal_id):
	# First of all we need the query to be sent to post
	# In the query parameters, you need to set the variables you define inside the fields first. So $search in media has a corresponding $search: String! in the query parameters
	# Their value is their type.
	query = '''
		query ($idMal: Int) {
			Media (idMal: $idMal, type: ANIME) {
				id
				title {
				english
				}
				averageScore
			}
		}
	'''

	variables = {
		'idMal': int(mal_id)
	}

	# Get the base url that we send the post request unto
	base_url = 'https://graphql.anilist.co'


	# Make the request

	response = requests.post(base_url, json={'query': query, 'variables': variables}) 

	if response.status_code == 200:
		data = response.json()

		anime_data = data["data"]["Media"]
		
		if not anime_data:
			raise ValueError(f"No results found for {mal_id}")
		
		return anime_data

	else:
		raise ConnectionError("Cannot connect to the database")

def get_anilist_score(mal_id):
    anime_data = get_anilist_data(mal_id)
    anilist_score = anime_data.get("averageScore") / 10.0
    return anilist_score