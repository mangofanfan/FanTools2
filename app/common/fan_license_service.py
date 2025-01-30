import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from requests_oauthlib import OAuth2Session, OAuth2


CLIENT_ID = "ezJIGWXZ0IsQBK5B4vKpvMLmmVxviWRJobPltU3B"
CLIENT_SECRET = "ixsz737HSUPTb59lKDV8sqESvY7VL1Yh1Fe5YWdX"
REDIRECT_URI = "http://localhost:8080/"

fanlive_url = "https://ifanspace.top/oauth/authorize"
fanlive_token = "https://ifanspace.top/oauth/token"
fanlive_me = "https://ifanspace.top/oauth/me"


if __name__ == "__main__":
    client = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    AUTH_URL, state = client.authorization_url(fanlive_url)

    print(AUTH_URL, state)

    AUTH_RES = input("full callback:")
    client.fetch_token(fanlive_token, client_secret=CLIENT_SECRET, authorization_response=AUTH_RES)

    res = client.get(fanlive_me)

    print(res.json())

    datas: dict = res.json()
    print(datas["zib_other_data"]["cover_image"])
    print(datas["zib_other_data"]["custom_avatar"])
