
from urllib.parse import urlencode
import requests
import json
from time import sleep

APP_ID = "6646096"
AUTH_SERVER = "https://oauth.vk.com/authorize"
auth_data = {
    "client_id": APP_ID,
    "display": "page",
    "redirect_url": "https://oauth.vk.com/blank.html",
    "scope": "status,friends,groups",
    "response_type": "token",
    "v": 5.80
}

id1 = 13575261
#Работа со статусами и получение токена
print("?".join((AUTH_SERVER, urlencode(auth_data))))
#TOKEN = "203d08492f2160e55c9af9a7587fec06666678eefe35ad258ac0e82b1cb64fe8de3e5aaa8b4c6528cb178"
TOKEN = "99fb9a4f034dc329f4d86efb6bfdae66452be73b4bdecc6ebf8449796ef73370dc165de4640f64618bebd"
status = requests.get("https://api.vk.com/method/status.get", params=dict(access_token=TOKEN, v=5.80))
print(status.text)

#запрашиваем список друзей
def get_VKfriends_by_id(VK_token):
    response = requests.get("https://api.vk.com/method/friends.get",
                            params=dict(access_token=VK_token, v=5.80))
    print(response.text)
    return response.json()["response"]['items']

#запрашиваем список групп
def get_VKgroups_by_id(VK_token):
    response = requests.get("https://api.vk.com/method/groups.get",
                            params=dict(access_token=VK_token, v=5.80))
    print(response.text)
    return response.json()["response"]['items']

#запрашиваем список юзеров из заданного сообщества с помощью особой функции
def get_friends_in_group(VK_token, group):
    users_in_group = requests.get("https://api.vk.com/method/groups.getMembers",
                            params=dict(access_token=VK_token, v=5.80, group_id=group, filter="friends"))
    print(f"В группе {group} обнаружилось {users_in_group.json()['response']['count']} друзей")
    return users_in_group.json()['response']['count']

friends_total = get_VKfriends_by_id(TOKEN)
groups_total = get_VKgroups_by_id(TOKEN)

result = list()
result_json = list()

for group_id in groups_total:
    print(group_id)
    if not get_friends_in_group(TOKEN, group_id):
        print(f"Группа {group_id} нам подходит")
        result.append(group_id)
    sleep(0.28)

print(result)

for i in result:
    tmp_dict = dict()
    response = requests.get("https://api.vk.com/method/groups.getById",
                        params=dict(access_token=TOKEN, v=5.80, group_id=i, fields="description,members_count"))
    print(response.json())
    tmp_dict["name"] = response.json()['response'][0]['name']
    tmp_dict["gid"] = response.json()['response'][0]['id']
    tmp_dict["members_count"] = response.json()['response'][0]['members_count']
    print(tmp_dict)
    result_json.append(tmp_dict)

print(result_json)

with open('groups.json', 'w') as outfile:
    json.dump(result_json, outfile)


