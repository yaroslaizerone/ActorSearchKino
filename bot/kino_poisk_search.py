import requests


def search_actor_by_name(name, api_key):
    url = f"https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=250&query={name}"

    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_actor_by_id(actor_id, api_key):
    url = f"https://api.kinopoisk.dev/v1.4/person/{actor_id}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_movie_by_id(movie_id, api_key):
    url = f"https://api.kinopoisk.dev/v1.4/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()