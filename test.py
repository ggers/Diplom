import main
from urllib.parse import urlencode
import requests
import json
from time import sleep

def get_by_id(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/users.get",
                            params=dict(access_token=VK_token, v=5.80, user_ids=user_id, fields="counters"))
    print(response.text)
    return

#get_by_id(main.TOKEN, 46298639)

def get_VKfriends_by_id(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/friends.get",
                            params=dict(access_token=VK_token, v=5.80, user_ids=user_id))
    print(f"У пользователя {user_id} обнаружилось целых {response.json()['response']['count']} друзей")
    return response.json()["response"]['items']



#запрашиваем список групп
def get_VKgroups_by_id(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/groups.get",
                            params=dict(access_token=VK_token, v=5.80, user_id=user_id))
    print(f"Пользователь {user_id} состоит в {response.json()['response']['count']} группах")
    return response.json()['response']['items']


def get_VKgroups_by_id2(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/groups.get",
                            params=dict(access_token=VK_token, v=5.80, user_id=user_id))
    try:
        x = response.json()['response']['items']
        return x
    except:
        print(f"Спешу уведомить, что ваш друг {user_id} от вас что-то скрывает!")
        return None


def get_friend_in_group(VK_token, group, user_id):
    response = requests.get("https://api.vk.com/method/groups.isMember",
                            params=dict(access_token=VK_token, v=5.80, user_id=user_id, group_id=group, extended=1))
    print(response.json())
    return bool(response.json()["response"]['member'])

def get_friend_in_group2(VK_token, group, user_ids):
    response = requests.get("https://api.vk.com/method/groups.isMember",
                            params=dict(access_token=VK_token, v=5.80, user_ids=user_ids, group_id=group))
    print(response['response'])
    return

list_friends = get_VKfriends_by_id(main.TOKEN, 13575261)
set_goups = set(get_VKgroups_by_id(main.TOKEN, 13575261))

#print(list_friends)
#print(set_goups)
friend_set = set_goups
result = set_goups
print(f"Сначала было {len(result)} элементов:\n  {result}")

for friend in list_friends:
    print(f"Обрабатываем друга {friend}")
    now = get_VKgroups_by_id2(main.TOKEN, friend)
    if now:
        friend_set = set(now)
#        print(friend_set)
    sleep(0.28)
    result.difference_update(friend_set)
    print(f"После этого цикла осталось {len(result)} элементов:\n")

