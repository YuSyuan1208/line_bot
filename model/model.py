import re
import requests
import json


def getLineProfile(body):
    json_dict = json.loads(body)
    # print(json_dict)

    headers = {
        "Content-Type": "application/json",
        "Authorization":
            "Bearer " + json_dict['access_token'],
    }
    # print(headers)
    # print(re_payload)

    url = "https://api.line.me/v2/profile"
    # re = requests.post(url, headers=headers, data=json.dumps(re_payload).encode("utf-8"), timeout=None)
    re = requests.get(url, headers=headers,  timeout=None)
    re_json = re.json()
    if re_json['userId'] == 'Ub95da38ba9b7324f35940beca4f7d01e':
        re_json['checkFlag'] = True
    else:
        re_json['checkFlag'] = False

    print(re_json)
    return json.dumps(re_json)


def checkAccount(body):
    """ 登入身分證、密碼確認，預設A123456789、123456 """
    json_dict = json.loads(body)
    if json_dict['帳號'] == 'A123456789' and json_dict['密碼'] == '123456':
        return {'checkAccountFlag': True}
    else:
        return {'checkAccountFlag': False}

def register_check(body):
    """ 註冊確認 """
    json_dict = json.loads(body)