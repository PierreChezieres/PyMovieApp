from dataframes import TAGS, TITLES, YEARS

def movies_to_str(movies):
    return [f"[{i}] {t} ({y})" for i, t, y in zip(movies, TITLES.loc[movies, 'title'], YEARS.loc[movies, 'year'])]

def movie_tags_info(id, level=6):
    tags = TAGS.loc[id,:]
    names = TAGS.columns
    selected_tags = list()
    for tag in names:
        relevance = tags[tag].item()
        if relevance>=level:
            selected_tags.append((tag, relevance))
    return sorted(selected_tags, key=lambda tag:tag[1], reverse=True)