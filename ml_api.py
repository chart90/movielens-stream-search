import requests
import json
import os
from urllib.parse import urlencode
import pickle as pkl
import config
from time import time


class MovieLens:
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'DNT': '1',
            'Host': 'movielens.org',
            'Pragma': 'no-cache',
        }
        self.core_url = 'https://movielens.org'
        self.auth_cookie = None
        self.get_auth_cookie()

    def set_auth_cookie(self, cookie):
        with open('config/cookies.pkl', 'wb') as f:
            pkl.dump(cookie, f)
        self.auth_cookie = cookie

    def get_auth_cookie(self):
        if os.path.isfile('config/cookies.pkl'):
            with open('config/cookies.pkl', 'rb') as f:
                auth_cookie = pkl.load(f)
            now = time()
            cookie_data = [k for k in auth_cookie][0]
            if cookie_data.expires > now:
                self.auth_cookie = auth_cookie
                return

        username = config.USERNAME
        password = config.PASSWORD
        cookie = self.login(username, password)
        if cookie is None:
            print('Invalid login! Please check username and password.')
        else:
            self.set_auth_cookie(cookie)

    def login(self, username, password):
        auth = {
            'userName': username,
            'password': password
        }
        auth = json.dumps(auth)

        path = '/api/sessions'
        url = self.core_url + path

        headers = self.headers
        headers['Referer'] = 'https://movielens.org/login'

        r = requests.post(url, data=auth, headers=headers)
        print(f'Request status: {r.status_code}, {r.text}')
        if r.json()['status'] == 'success':
            return r.cookies
        return None

    def request_getter(self, path, query_str=''):
        url = self.core_url + path + '?' + query_str

        req = requests.get(url, cookies=self.auth_cookie)
        res = req.json()
        if res['status'] == 'success':
            res = res['data']
        return res

    def get_genres(self):
        return self.request_getter('/api/movies/genres')

    def get_me(self):
        return self.request_getter('/api/users/me')

    def get_mytags(self):
        return self.request_getter('/api/users/me/tags')

    def explore(self, params):
        return self.request_getter('/api/movies/explore', urlencode(params))

    def top_picks(self):
        params = {
            'hasRated': 'no',
            'sortBy': 'prediction'
        }
        return self.explore(params)
