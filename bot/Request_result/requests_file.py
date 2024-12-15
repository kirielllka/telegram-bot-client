import asyncio
from wsgiref.util import application_uri

import requests

start_url = 'http://127.0.0.1:8000/api/'
token = 'd49d43a85d531bca57c2830bbfde826eebaf0d6e'
headers={'Content-type':'application/json','Authorization':f'Token {token}'}
#def get_all_posts():
 #   posts = requests.get(f'{start_url}+posts', headers={Autorization:''})
  #  print(posts)

# async def registration(email, login, password):
#    data = {
#        'email':email,
#        'username':login,
#        'password':password
#    }
#    result = requests.post(f'{start_url}+auth/users/', data=data)
#     print(result)
class BaseResponces:
    @staticmethod
    async def get_all_posts(token):
        try:
            headers = {'Content-type': 'application/json', 'Authorization': f'Token {token}'}
            return requests.get(f'{start_url}v1/posts', headers=headers).json()
        except Exception:
            return {'Responce':'error'}

    @staticmethod
    async def retriev_post(id:int,token):
        try:
            headers = {'Content-type': 'application/json', 'Authorization': f'Token {token}'}
            return requests.get(f'{start_url}v1/posts/{id}', headers=headers).json()
        except Exception:
            return {'Responce':'error'}

    @staticmethod
    async def posts_search(info:str, token):
        try:
            headers = {'Content-type': 'application/json', 'Authorization': f'Token {token}'}
            return requests.get(f'{start_url}v1/posts/?search={info}', headers=headers).json()
        except Exception:
            return {'Responce':'error'}

    @staticmethod
    async def comments_on_post(id: int, token):
        try:
            headers = {'Content-type': 'application/json', 'Authorization': f'Token {token}'}
            return requests.get(f'{start_url}v1/posts/{id}/comments/', headers=headers).json()
        except Exception:
            return {'Responce':'error'}

    @staticmethod
    async def get_profile(id: int, token):
        try:
            headers = {'Content-type': 'application/json', 'Authorization': f'Token {token}'}
            return requests.get(f'{start_url}v1/profiles/{id}', headers=headers).json()
        except Exception:
            return {'Responce':'error'}

    @staticmethod
    async def get_posts_by_user(id:int, token):
        try:
            headers = {'Content-type': 'application/json', 'Authorization': f'Token {token}'}
            return requests.get(f'{start_url}v1/posts/?author={id}', headers=headers).json()
        except Exception:
            return {'Responce':'error'}

    @staticmethod
    async def register(data):
        try:
            request = requests.post(f'{start_url}auth/users/', data=data).json()
        except Exception:
            return 'Error'

    @staticmethod
    async def login(data):
        try:
            request = requests.post(f'{start_url}auth/token/login/', data=data).json()
            return request['auth_token']
        except Exception:
            return 'Error'






