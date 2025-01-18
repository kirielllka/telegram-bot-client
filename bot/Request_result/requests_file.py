

import requests
from urllib3 import request

start_url = "http://127.0.0.1:8000/api/"



class BaseResponces:
    @staticmethod
    async def get_all_posts(token):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            return requests.get(f"{start_url}v1/posts/", headers=headers).json()
        except Exception:

            return {"Responce": "error"}

    @staticmethod
    async def retriev_post(id: int, token):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            return requests.get(f"{start_url}v1/posts/{id}", headers=headers).json()
        except Exception:
            return {"Responce": "error"}

    @staticmethod
    async def posts_search(info: str, token):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            return requests.get(f"{start_url}v1/posts/?search={info}", headers=headers).json()
        except Exception:
            return {"Responce": "error"}

    @staticmethod
    async def comments_on_post(id: int, token):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            return requests.get(f"{start_url}v1/posts/{id}/comments/", headers=headers).json()
        except Exception:
            return {"Responce": "error"}

    @staticmethod
    async def get_profile(id: int, token):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            return requests.get(f"{start_url}v1/profiles/{id}", headers=headers).json()
        except Exception:
            return {"Responce": "error"}

    @staticmethod
    async def get_posts_by_user(id: int, token):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            return requests.get(f"{start_url}v1/posts/?author={id}", headers=headers).json()
        except Exception:
            return {"Responce": "error"}

    @staticmethod
    async def register(data):
        try:
            request = requests.post(f"{start_url}auth/users/", data=data).json()
            print(request)
        except Exception:
            return "Error"

    @staticmethod
    async def login(data):
        try:
            request = requests.post(f"{start_url}auth/token/login/", data=data).json()
            return request["auth_token"]
        except Exception:
            return "Error"

    @staticmethod
    async def create_post(data, token):
        try:
            request = requests.post(
                f"{start_url}v1/posts/",
                json=dict(data),  # Сериализуем как JSON
                headers={"Content-type": "application/json", "Authorization": f"Token {token}"},
            )
            request.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
            return request.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    async def create_comment(data, post_id, token):
        try:
            request = requests.post(
                f"{start_url}v1/posts/{post_id}/comments/",
                json=data,
                headers={"Content-type": "application/json", "Authorization": f"Token {token}"},
            ).json()
            return request
        except Exception:
            return "Error"

    @staticmethod
    async def delete_post(post_id, token):
        try:
            request = requests.delete(
                f"http://127.0.0.1:8000/api/v1/posts/{post_id}/",
                headers={"Content-type": "application/json", "Authorization": f"Token {token}"},
            ).json()
            print(request)


            return "Error"
        except Exception:
            return request

    @staticmethod
    async def user_me(token):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            req= requests.get(f"{start_url}auth/users/me", headers=headers).json()
            print(req)
            return req

        except Exception:
            return {"Responce": "error"}

    @staticmethod
    async def red_profile(token,user_id,data):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            req = requests.put(f"{start_url}v1/profiles/{user_id}/", headers=headers, json=data).json()
            return req
        except Exception:
            return 'Error'

    @staticmethod
    async def red_post(token, user_id, data):
        try:
            headers = {"Content-type": "application/json", "Authorization": f"Token {token}"}
            req = requests.put(f"{start_url}v1/posts/{user_id}/", headers=headers, json=data).json()
            return req
        except Exception:
            return 'Error'

