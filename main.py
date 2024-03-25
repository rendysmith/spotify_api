import requests
from constants import CLIENT_ID, CLIENT_SECRET, USER_ID

"https://developer.spotify.com/documentation/web-api/reference/create-playlist"

def get_token():
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.json())

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Failed to get access token:", response.text)
        return None


def get_profile():
    """curl --request GET \
  --url https://api.spotify.com/v1/me \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'"""

    url = 'https://api.spotify.com/v1/me'

    headers = {
        'Authorization': f'Bearer {get_token()}'

    }

    response = requests.get(url, headers=headers)
    r_json = response.json()
    print(r_json)


get_profile()


def create_playlist(name_playlist):

    """curl --request POST \
  --url https://api.spotify.com/v1/users/smedjan/playlists \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z' \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "New Playlist",
    "description": "New playlist description",
    "public": false
}'"""
    token = get_token()
    print(token)

    url = f'https://api.spotify.com/v1/users/{USER_ID}/playlists'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        "name": name_playlist,
        "description": "New playlist description",
        "public": False
    }

    response = requests.post(url, headers=headers, json=data)
    r_json = response.json()
    print(r_json)

    status_code = response.status_code

    if status_code == 200:
        print(r_json)

    elif status_code == 403:
        print(r_json['error']['message'])
        print('Этот запрос требует аутентификации пользователя.')



    else:
        print("Failed to get access token:", response.text)

#create_playlist("1111111111333333335555555555")

