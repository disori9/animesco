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

if __name__ == '__main__':
    app.run(debug=True)