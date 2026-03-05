from anilist_results import get_anilist_recommendations
from mal_results import get_mal_recommendations


def get_smart_recommendations(mal_id):
    mal_recs = get_mal_recommendations(mal_id)
    ani_recs = get_anilist_recommendations(mal_id)
    
    combined = {}
    
    # 1. Process MAL recs
    for item in mal_recs:
        current_id = item['mal_id']
        # Add a custom 'score' key. Let's just use MAL votes as the base score.
        item['smart_score'] = item['votes'] 
        combined[current_id] = item
        
    # 2. Process AniList recs
    for item in ani_recs:
        current_id = item['mal_id']
        
        # Did MAL also recommend this?
        if current_id in combined:
            combined[current_id]['smart_score'] += (item['votes'] + 100)
            
        else:
            item['smart_score'] = item['votes']
            combined[current_id] = item
            
            
    # 3. Convert dictionary values back to a list
    final_list = list(combined.values())
    
    # 4. Sort the list by 'smart_score' descending
    final_list.sort(key=lambda x: x['smart_score'], reverse=True)
    
    return final_list # Return the top 10 absolute best

if __name__ == "__main__":
    try:
        test_data = get_smart_recommendations(37430)

        for item in test_data:
            print(f"{item['title']}: {item['smart_score']}")
            
    except Exception as e:
        print(f"Error: {e}")