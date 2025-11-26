from anilist_results import get_anilist_score
from mal_results import  get_mal_score
from get_title import get_verified_title

anime_title = get_verified_title()
anilist_score = get_anilist_score(anime_title)
mal_score = get_mal_score(anime_title)

print(f"Anilist: {anilist_score}")
print(f"MAL: {mal_score}")

mean_score = (anilist_score + mal_score) / 2
mean_score = round(mean_score, 2)
print(f"Final score: {mean_score}")