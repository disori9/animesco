from flask import Flask, render_template, request
from get_title import top_search_results
from mal_results import *
from anilist_results import *
from recommender import *
import time

app = Flask(__name__)

# This function runs when someone visits the homepage '/'
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form['anime_title']
    titles = top_search_results(user_input)
    return render_template('search_results.html', titles=titles)

@app.route('/score', methods=['POST'])
def score():
    try:
        anime_title = request.form['anime_title']
        mal_id = request.form['mal_id']
        mal_data = get_anime_by_id(mal_id)
        
        mal_score = mal_data.get("score")
        mal_cover = mal_data["images"]["jpg"]["image_url"]
        mal_status = mal_data["status"]
        mal_episodes = mal_data["episodes"]
        mal_date = mal_data["aired"]["string"]
        eng_title = mal_data["title_english"]
        trailer_url = mal_data.get('trailer', {}).get('embed_url')

        mal_genres = []
        for genre in mal_data["genres"]:
            mal_genres.append(genre["name"])

        synopsis = mal_data["synopsis"]

        anilist_score = get_anilist_score(mal_id)
        
        average_score = (mal_score + anilist_score) / 2

        recommendations = get_smart_recommendations(mal_id)
        
        return render_template('selected_anime.html', anime_title=anime_title, average_score=average_score, mal_cover=mal_cover,
                               mal_score=mal_score, anilist_score=anilist_score, synopsis=synopsis, mal_status=mal_status, mal_genres=mal_genres,
                               mal_episodes=mal_episodes, mal_date=mal_date,
                               recommendations=recommendations, eng_title=eng_title, trailer_url=trailer_url,)
    except ValueError as e:
        return f"<h1>Error</h1> <p>{e}</p> <a href='/'>Go Back</a>"
    except Exception as e:
        return f"<h1>System Error</h1> <p>Something went wrong: {e}</p> <a href='/'>Go Back</a>"


@app.route('/combiner')
def combiner_page():
    return render_template('combiner.html')

@app.route('/smart_combine', methods=['POST'])
def smart_combine():
    # 1. Grab raw inputs
    raw_inputs = [
        {'id': request.form.get('anime1_id'), 'title': request.form.get('anime1_title')},
        {'id': request.form.get('anime2_id'), 'title': request.form.get('anime2_title')},
        {'id': request.form.get('anime3_id'), 'title': request.form.get('anime3_title')}
    ]
    
    # FIX 1: Filter out any empty inputs (for when they only pick 2 shows)
    input_shows = []
    for show in raw_inputs:
        if show['id']: # If id is not empty
            input_shows.append({'id': int(show['id']), 'title': show['title']})
            
    input_ids = [show['id'] for show in input_shows]
    max_overlap = len(input_shows) # Will be either 2 or 3

    # 2. THE SAFE FETCH
    all_recommendations = []
    for show in input_shows:
        url = f"https://api.jikan.moe/v4/anime/{show['id']}/recommendations"
        response = requests.get(url)
        if response.status_code == 200:
            all_recommendations.append(response.json().get('data', []))
        time.sleep(0.5) 

    # 3. BUILD THE MASTER DICTIONARY
    master_dict = {}
    for i, rec_list in enumerate(all_recommendations):
        source_title = input_shows[i]['title'] 
        
        for rec in rec_list:
            entry = rec['entry']
            rec_id = entry['mal_id']
            votes = rec['votes']

            if rec_id in input_ids:
                continue

            if rec_id not in master_dict:
                master_dict[rec_id] = {
                    'mal_id': rec_id,
                    'title': entry['title'],
                    'cover': entry['images']['jpg']['large_image_url'],
                    'base_score': votes,
                    'appearance_count': 1,
                    'recommended_by': [source_title] 
                }
            else:
                master_dict[rec_id]['base_score'] += votes
                master_dict[rec_id]['appearance_count'] += 1
                if source_title not in master_dict[rec_id]['recommended_by']:
                    master_dict[rec_id]['recommended_by'].append(source_title)

    # 4. APPLY MULTIPLIERS (FIX 2: Dynamic Math)
    final_results = []
    for rec_id, data in master_dict.items():
        
        if data['appearance_count'] == max_overlap:
            final_score = int(data['base_score'] * 1.5) # Perfect overlap (2/2 or 3/3)
        elif max_overlap == 3 and data['appearance_count'] == 2:
            final_score = int(data['base_score'] * 1.2) # Partial overlap (2/3)
        else:
            final_score = data['base_score']

        if final_score > 0:
            final_results.append({
                'mal_id': data['mal_id'],
                'title': data['title'],
                'cover': data['cover'],
                'smart_score': final_score,
                'overlap': data['appearance_count'],
                'recommended_by': data['recommended_by'] 
            })

    final_results = sorted(final_results, key=lambda x: x['smart_score'], reverse=True)[:20]

    # Pass max_overlap to the template so the UI knows if 2 means "perfect" or "partial"
    return render_template('combiner_results.html', recommendations=final_results, max_overlap=max_overlap)
if __name__ == '__main__':
    app.run(debug=True)