
from requests_file import BaseResponces


class BaseReformat:
    @staticmethod
    async def all_posts():
        data = await BaseResponces.get_all_posts()
        result = {}
        for post in data:
            result[post["id"]](
                f"{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n"
                f"❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}"
            )
        return result

    @staticmethod
    async def retrieve_post(id: int):
        data = await BaseResponces.retriev_post(id=id)
        result = (
            f"{data['title']}\n{data['content']}\nАвтор:{data['autor_info']['username']}\n"
            f"❤️{data['like_count']}\nДата создания:{data['created_at'][:10]}"
        )
        return result

    @staticmethod
    async def posts_search(info: str):
        data = await BaseResponces.posts_search(info)
        result = []
        for post in data:
            result.append(
                f"{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n"
                f"❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}"
            )
        return result

    @staticmethod
    async def comments_on_post(id: int):
        data = await BaseResponces.comments_on_post(id)
        result = []
        for post in data["results"]:
            result.append(
                f"{post['title']}\n{post['content']}\nАвтор:{post['user_info']['username']}\n"
                f"❤️{post['like_count']}\nДата создания:{post['date_of_create'][:10]}"
            )
        return result

    @staticmethod
    async def get_profile(id):
        data = await BaseResponces.get_profile(id)
        for val in data.values():
            if val is None or val == 0:
                val = "не известно"
        result = f"{data['full_name']}\n{data['user_patronymic']}\n{data['age']}\n{data['user_birth_date']}"
        return result

    @staticmethod
    async def get_post_by_user(id):
        data = await BaseResponces.get_posts_by_user(id)
        result = []
        for post in data:
            result.append(
                f"{post['title']}\n{post['content']}\nАвтор:{post['autor_info']['username']}\n❤️{post['like_count']}\nДата создания:{post['created_at'][:10]}"
            )
        return result


async def main():
    post_data = await BaseReformat.retrieve_post(1)
    print(post_data)


