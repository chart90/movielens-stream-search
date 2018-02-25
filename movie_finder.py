from justwatch import JustWatch
from ml_api import MovieLens
import json

ml = MovieLens()
jw = JustWatch(country='GB')

DEFAULT_FILTERS = {
    'monetization_type': ('rent', 'buy', 'cinema'),
    'provider_id': None
}

with open('providers.json', 'r') as f:
    PROVIDERS = json.load(f)
PROVIDERS = {int(key): val for key, val in PROVIDERS.items()}


def get_correct_movie(res, id_val):
    for candidate in res['items']:
        id_src = candidate['scoring']
        tmdb_id = [id_type
                   for id_type in id_src
                   if id_type['provider_type'] == 'tmdb:id']
        if len(tmdb_id) > 0:
            tmdb_id = tmdb_id[0]['value']
            if tmdb_id == id_val:
                return candidate
    return None


def get_available_streams(jw_movie, filters):
    offers = list()
    for offer in jw_movie.get('offers', []):
        if all([offer[f_key] not in f_vals
                for f_key, f_vals in filters.items()]):
            service = PROVIDERS.get(offer['provider_id'], 'UNKNOWN')
            url = offer['urls']['standard_web']
            if any([service == of['service'] for of in offers]):
                continue
            offers.append({
                'service': service,
                'url': url
            })
    return offers


def return_top_list(search_query, filters=DEFAULT_FILTERS, results_size=10):
    results_list = []
    page_no = 1
    while len(results_list) < results_size:
        search_query['page'] = page_no
        search_res = ml.explore(search_query)
        for mv in search_res['searchResults']:
            movie_title = mv['movie']['title']
            movie_record = {
                'id': mv['movie']['tmdbMovieId'],
                'title': mv['movie']['title'],
                'genres': mv['movie']['genres'],
                'avgRating': mv['movie']['avgRating'],
                'myRating': mv['movieUserData']['prediction']
            }
            jw_movies = jw.search_for_item(query=movie_record['title'])
            jw_movie = get_correct_movie(jw_movies, movie_record['id'])
            if jw_movie is None:
                print(f"No JustWatch record found for {movie_title}")
                continue
            movie_record['description'] = jw_movie['short_description']
            streams = get_available_streams(jw_movie, filters)
            if len(streams) < 1:
                print(f"No streaming sites found for {movie_title}")
                continue
            movie_record['sources'] = streams
            results_list.append(movie_record)
        page_no += 1
    return results_list[:results_size]


if __name__ == '__main__':
    query = {
        'hasRated': 'no',
        'sortBy': 'prediction'
    }
    filter_dict = DEFAULT_FILTERS
    filter_dict['provider_id'] = (29, 39)
    print(json.dumps(return_top_list(query, results_size=10), indent=4))
