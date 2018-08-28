
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
id2 = 171691064
#получение токена
print("?".join((AUTH_SERVER, urlencode(auth_data))))
#TOKEN = "203d08492f2160e55c9af9a7587fec06666678eefe35ad258ac0e82b1cb64fe8de3e5aaa8b4c6528cb178"
TOKEN = "99fb9a4f034dc329f4d86efb6bfdae66452be73b4bdecc6ebf8449796ef73370dc165de4640f64618bebd"


#запрашиваем список друзей
def get_VKfriends_by_id(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/friends.get",
                            params=dict(access_token=VK_token, v=5.80, user_ids=user_id))
    print(f"У пользователя {user_id} обнаружилось целых {response.json()['response']['count']} друзей")
    return response.json()["response"]['items']

#запрашиваем список групп
def get_VKgroups_by_id(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/groups.get",
                            params=dict(access_token=VK_token, v=5.80, user_id=user_id))
    try:
        x = response.json()['response']['items']
        return x
    except:
        print(f"Спешу уведомить, что ваш друг {user_id} от вас что-то скрывает!")
        return None

#упрощенное решение задачи для пользователя связанного с токеном
def get_friends_in_group(VK_token, group):
    users_in_group = requests.get("https://api.vk.com/method/groups.getMembers",
                            params=dict(access_token=VK_token, v=5.80, group_id=group, filter="friends"))
    print(f"В группе {group} обнаружилось {users_in_group.json()['response']['count']} друзей\n")
    return users_in_group.json()['response']['count']

#запрашиваем информацию о группе по её идентификатору
def get_group_info_by_id(VK_token, list_group):
    for i in list_group:
        tmp_dict = dict()
        response = requests.get("https://api.vk.com/method/groups.getById",
                         params=dict(access_token=VK_token, v=5.80, group_id=i, fields="description,members_count"))
    #     print(response.json())
        tmp_dict["name"] = response.json()['response'][0]['name']
        tmp_dict["gid"] = response.json()['response'][0]['id']
        tmp_dict["members_count"] = response.json()['response'][0]['members_count']
        print(tmp_dict)
        result_json.append(tmp_dict)
    print(result_json)
    return result_json

def difficult_way():
    list_friends = get_VKfriends_by_id(TOKEN, 171691064)
    set_goups = set(get_VKgroups_by_id(TOKEN, 171691064))

    # print(list_friends)
    # print(set_goups)
    friend_set = set_goups
    result = set_goups
    print(f"Сначала было {len(result)} элементов:\n  {result}")

    for friend in list_friends:
        print(f"Обрабатываем друга {friend}")
        now = get_VKgroups_by_id(TOKEN, friend)
        if now:
            friend_set = set(now)
        #        print(friend_set)
        sleep(0.28)
        result.difference_update(friend_set)
        print(f"После этого цикла осталось {len(result)} элементов:\n")
    print(f"В конце порлучилось {len(result)} элементов:\n  {result}")
    return result

def easy_way():

    groups_total = get_VKgroups_by_id(TOKEN, 171691064)
    result = list()
    for group_id in groups_total:
        if not get_friends_in_group(TOKEN, group_id):
            print(f"Группа {group_id} нам подходит \n")
            result.append(group_id)
        sleep(0.28)
    print(result)
    return result

def collect_data (result):

    result_json = list()
    for i in result:
        tmp_dict = dict()
        response = requests.get("https://api.vk.com/method/groups.getById",
                        params=dict(access_token=TOKEN, v=5.80, group_id=i, fields="description,members_count"))
#        print(response.json())
        tmp_dict["name"] = response.json()['response'][0]['name']
        tmp_dict["gid"] = response.json()['response'][0]['id']
        tmp_dict["members_count"] = response.json()['response'][0]['members_count']
#        print(tmp_dict)
        result_json.append(tmp_dict)
    print(result_json)
    return result_json


if __name__ == '__main__':
    print(f"Добро пожаловать в Скайнет v. 0.311")
    print(f"В настоящее время получен доступ к данным социальной сети VK.\n ")
    print(f"Вы можете ввести свой идентификатор, либо чужой и узнать, в каких группах состоит этот пользователь без своих друзей\n ")
    user_id = input(" > ")
    i = difficult_way()
    collect_data(i)






    #
    # with open('groups.json', 'w', encoding="utf-8") as outfile:
    #     json.dump(result_json, outfile)


