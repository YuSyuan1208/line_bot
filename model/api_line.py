import requests

def getProfileFromAccessToken(accessToken):
    """ accessToken獲取Line個人資訊 """
    headers = {
        "Content-Type": "application/json",
        "Authorization":
            "Bearer " + accessToken,
    }
    # print(headers)
    # print(re_payload)

    url = "https://api.line.me/v2/profile"
    # re = requests.post(url, headers=headers, data=json.dumps(re_payload).encode("utf-8"), timeout=None)
    re = requests.get(url, headers=headers,  timeout=None)
    return re.json()