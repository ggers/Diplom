
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
TOKEN = "99fb9a4f034dc329f4d86efb6bfdae66452be73b4bdecc6ebf8449796ef73370dc165de4640f64618bebd"


#запрашиваем список друзей
def get_VKfriends_by_id(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/friends.get",
                            params=dict(access_token=VK_token, v=5.80, user_ids=user_id))
    print(f"User number {user_id} have total {response.json()['response']['count']} friends")
    return response.json()["response"]['items']

#запрашиваем список групп
def get_VKgroups_by_id(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/groups.get",
                            params=dict(access_token=VK_token, v=5.80, user_id=user_id))
    try:
        x = response.json()['response']['items']
        return x
    except:
        print(f"Have no access to user {user_id}. He hides something from you...")
        return None

#упрощенное решение задачи для пользователя связанного с токеном
def get_friends_in_group(VK_token, group):
    users_in_group = requests.get("https://api.vk.com/method/groups.getMembers",
                            params=dict(access_token=VK_token, v=5.80, group_id=group, filter="friends"))
    print(f"Target group {group} consists {users_in_group.json()['response']['count']} friends\n")
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

def difficult_way(id):
    list_friends = get_VKfriends_by_id(TOKEN, id)
    set_goups = set(get_VKgroups_by_id(TOKEN, id))
    friend_set = set_goups
    result = set_goups
    print(f"Firstly we have {len(result)} elements:\n  {result}")

    for friend in list_friends:
        print(f"Checking friend number {friend}")
        now = get_VKgroups_by_id(TOKEN, friend)
        if now:
            friend_set = set(now)
        sleep(0.28)
        result.difference_update(friend_set)
        print(f"Now we have only {len(result)} secret groups:\n")
    print(f"Finally we have {len(result)} elements:\n  {result}")
    return result

def easy_way(id):
    groups_total = get_VKgroups_by_id(TOKEN, id)
    result = list()
    for group_id in groups_total:
        if not get_friends_in_group(TOKEN, group_id):
            print(f"Group {group_id} is for your eyes only.\n")
            result.append(group_id)
        sleep(0.28)
    print(result)
    return result

def collect_data(result):
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
        sleep(0.28)
    print(result_json)
    return result_json

def export_data_to_file(filename, data):
    with open(filename, 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile)

def get_user_id():
    while True:
        user_id = input(" > ")
        if user_id.isdigit():
            print(f"Initialising spy action for user {user_id}")
            break
        else:
            print(f"ERROR!")
    return user_id

def validate_main_user(VK_token, user_id):
    response = requests.get("https://api.vk.com/method/users.isAppUser",
                            params=dict(access_token=VK_token, v=5.80, user_id=user_id))
    return response.json()['response']

if __name__ == '__main__':
    print(f"Welcome to SkyNet v. 0.311\n")
    print(f"Now we have access to social net VK.\n Input your id")
    i = get_user_id()
    if validate_main_user(TOKEN, i):
        print(f"YOUR Account secrets you can see in 'secret.json' file\n")
        export_data_to_file('secret.json', collect_data(easy_way(i)))
    else:
        print(f"Access denied!\n")
    print(f"Input user id to access this user secret groups\n")
    j = get_user_id()
    if get_VKgroups_by_id(TOKEN, j):
        export_data_to_file('groups.json', collect_data(difficult_way(j)))
    else:
        print(f"Access denied!\n")

