

async def Token_add(token,user_id):
    with open('/home/yanix/Desktop/Tokens_tg.txt', 'a')  as file:
        if await Token_search(user_id,token):
            print('Token change or match')
        file.write(f'{user_id} {token}')
        print('Token save')

def Token_fill():
    with open('/home/yanix/Desktop/Tokens_tg.txt', 'r') as file:
        tokens = {}
        for line in file.readlines():
            print(line[:-1].split(' '))
            tokens[int(line.split(' ')[0])] = line.split(' ')[1][:-1]
        return tokens


async def Token_search(user_id,token):
    with open('/home/yanix/Desktop/Tokens_tg.txt') as file:
        for line in file.readlines():
            if line.split(' ')[0] == user_id: line.split(' ')[1] = token
            return True


async def logout(user_id):
    file_path = '/home/yanix/Desktop/Tokens_tg.txt'
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if int(line.split(' ')[0]) != user_id:
                    file.write(line)
        print(f"Удаление токена пользователя с id: {user_id} завершено")
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

