from flask import Flask, render_template, request
from get_title import top_search_results
from mal_results import *
from anilist_results import *

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
        
        mal_genres = []
        for genre in mal_data["genres"]:
            mal_genres.append(genre["name"])

        synopsis = mal_data["synopsis"]

        anilist_score = get_anilist_score(mal_id)
        
        average_score = (mal_score + anilist_score) / 2
        
        return render_template('selected_anime.html', anime_title=anime_title, average_score=average_score, mal_cover=mal_cover,
                               mal_score=mal_score, anilist_score=anilist_score, synopsis=synopsis, mal_status=mal_status, mal_genres=mal_genres,
                               mal_episodes=mal_episodes, mal_date=mal_date)
    except ValueError as e:
        return f"<h1>Error</h1> <p>{e}</p> <a href='/'>Go Back</a>"
    except Exception as e:
        return f"<h1>System Error</h1> <p>Something went wrong: {e}</p> <a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(debug=True)