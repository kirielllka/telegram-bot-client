

def Token_add(token,user_id):
    with open('/home/yanix/Desktop/Tokens_tg.txt', 'w')  as file:
        if Token_search(user_id,token):
            print('Token change or match')
            return None
        file.write(f'{user_id} {token}')
        print('Token save')

def Token_fill():
    with open('/home/yanix/Desktop/Tokens_tg.txt', 'r') as file:
        tokens = {}
        for line in file.readlines():
            tokens[int(line.split(' ')[0])] = line.split(' ')[1]
        return tokens


def Token_search(user_id,token):
    with open('/home/yanix/Desktop/Tokens_tg.txt') as file:
        for line in file.readlines():
            if line.split(' ')[0] == user_id: line.split(' ')[1] = token
            return True