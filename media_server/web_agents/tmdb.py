import requests
import urllib.parse
import shutil

# use 'append to reponse' for multiple requests in same namespace

# TODO /tv/{tv_id}/episode_groups, /tv/episode_group/{id} for episode orders

class TmdbClient:
    api_key = 'ff18711eedb84dca2e96457ddb4c09f6'
    base_url = 'https://api.themoviedb.org/3/'
    config = {}

    def __init__(self) -> None:
        self.config = self.configure()

    def configure(self):
        path = 'configuration'
        url = urllib.parse.urljoin(self.base_url, path)
        params = {
            'api_key': self.api_key,
        }

        res = requests.get(url, params)
        res.raise_for_status()
        data = res.json()

        return data

    def search_tv_show(self, query, first_air_date_year=None):
        path = 'search/tv'
        url = urllib.parse.urljoin(self.base_url, path)
        params = {
            'query': query,
            'api_key': self.api_key,
            'first_air_date_year': first_air_date_year,
        }

        res = requests.get(url, params)
        res.raise_for_status()
        data = res.json()
        
        if data['results']:
            id: int = data['results'][0]['id']
            return id

        else:
            return None

    def tv_show(self, tmdb_tv_id):
        path = f'tv/{tmdb_tv_id}'
        url = urllib.parse.urljoin(self.base_url, path)
        params = {
            'api_key': self.api_key,
        }

        res = requests.get(url, params)

        if not res.ok:
            return None
        
        data = res.json()

        return data

    def tv_season(self, tmdb_tv_id, season_number):
        path = f'tv/{tmdb_tv_id}/season/{season_number}'
        url = urllib.parse.urljoin(self.base_url, path)
        params = {
            'api_key': self.api_key,
        }

        res = requests.get(url, params)

        if not res.ok:
            return None

        data = res.json()

        return data

    def tv_episode(self, tmdb_tv_id, season_number, episode_number):
        path = f'tv/{tmdb_tv_id}/season/{season_number}/episode/{episode_number}'
        url = urllib.parse.urljoin(self.base_url, path)
        params = {
            'api_key': self.api_key,
        }

        res = requests.get(url, params)

        if not res.ok:
            return None
            
        data = res.json()

        return data

    def search_movie(self, query, year=None):
        path = 'search/movie'
        url = urllib.parse.urljoin(self.base_url, path)
        params = {
            'query': query,
            'api_key': self.api_key,
            'year': year,
        }

        res = requests.get(url, params)
        res.raise_for_status()
        data = res.json()

        if data['results']:
            id: int = data['results'][0]['id']
            return id

        else:
            return None

    def movie(self, tmdb_movie_id):
        path = f'movie/{tmdb_movie_id}'
        url = urllib.parse.urljoin(self.base_url, path)
        params = {
            'api_key': self.api_key,
        }

        res = requests.get(url, params)
        res.raise_for_status()
        data = res.json()

        return data

    def download_image(self, tmdb_image_path):
        image_url = urllib.parse.urljoin(self.config['images']['secure_base_url'], 'original' + tmdb_image_path)
        filename = urllib.parse.urlsplit(image_url).path.split('/')[-1]

        with requests.get(image_url, stream=True) as res:
            res.raise_for_status()
            
            with open(filename, 'wb') as file:
                shutil.copyfileobj(res.raw, file)  # type: ignore

    def image_url(self, tmdb_image_path):
        if not tmdb_image_path:
            return None

        assert tmdb_image_path.startswith('/')
        return urllib.parse.urljoin(self.config['images']['secure_base_url'], 'original' + tmdb_image_path)
