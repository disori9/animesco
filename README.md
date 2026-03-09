# Animesco 🧭

Animesco is a lightweight, fast, and responsive web application built with Python and Flask. It aggregates data from multiple anime databases to provide users with deep analytics, high-fidelity recommendations, and algorithmic overlap calculations.

## 🚀 Features

* **Search Engine:** Queries the Jikan (MyAnimeList) and AniList APIs simultaneously to aggregate scores, statuses, and genres into a single unified dashboard.
* **Cinematic Trailer Modal:** Integrates a responsive, dynamic YouTube player overlay allowing users to watch trailers without leaving the application.
* **The Recommend Engine:** A custom algorithmic tool that takes 2 to 3 user-selected shows, fetches their individual recommendation arrays via parallel processing, and applies a weighted multiplier to find the ultimate intersection of overlapping recommendations.
* **Client-Side Fetching:** Utilizes asynchronous JavaScript fetching to create a smooth, staging-area UI without requiring full-page server reloads.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3 (Custom Flexbox/Grid UI), Vanilla JavaScript
* **APIs:** Jikan REST API (v4), AniList GraphQL API

## 💻 Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/animelens.git
   cd animelens
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On Mac/Linux: source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`.