import sqlite3
from anilist_results import get_anilist_score
from mal_results import  get_mal_score
from get_title import get_verified_title

# define connection and cursor for database
connection = sqlite3.connect("anime_data.db")

cursor = connection.cursor()

create_table_command = """CREATE TABLE IF NOT EXISTS anime_scores (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    mal_score REAL,
    anilist_score REAL,
    mean_score REAL
);"""

cursor.execute(create_table_command)


anime_title = get_verified_title()
anilist_score = get_anilist_score(anime_title)
mal_score = get_mal_score(anime_title)

print(f"Anilist: {anilist_score}")
print(f"MAL: {mal_score}")

mean_score = (anilist_score + mal_score) / 2
mean_score = round(mean_score, 2)
print(f"Final score: {mean_score}")

insert_data_command = """INSERT INTO anime_scores
	(title, anilist_score, mal_score, mean_score)
 	VALUES (?, ?, ?, ?)"""

data_to_insert = (anime_title, anilist_score, mal_score, mean_score)

cursor.execute(insert_data_command, data_to_insert)

connection.commit()
connection.close()