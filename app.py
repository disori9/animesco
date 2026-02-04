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
    return render_template('results.html', titles=titles)

@app.route('/score', methods=['POST'])
def score():
    try:
        anime_title = request.form['anime_title']

        mal_score = get_mal_score(anime_title)
        anilist_score = get_anilist_score(anime_title)
        
        average_score = (mal_score + anilist_score) / 2
        
        return f"{anime_title}: {average_score} rating."
    except ValueError as e:
        return f"<h1>Error</h1> <p>{e}</p> <a href='/'>Go Back</a>"
    except Exception as e:
        return f"<h1>System Error</h1> <p>Something went wrong: {e}</p> <a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(debug=True)