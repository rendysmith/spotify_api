import requests
import json

import selenium.common.exceptions
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#from bs4 import BeautifulSoup

from constants import CLIENT_ID, CLIENT_SECRET, USER_ID

"https://developer.spotify.com/documentation/web-api/reference/create-playlist"
"https://spotipy.readthedocs.io/en/2.22.1/"


def get_playlist_from_url(url):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)

    tracks = driver.find_elements(By.CSS_SELECTOR, "div[class='rounded-lg flex p-2 md:hover:bg-gray-50 justify-between']")

    print(len(tracks))

    tracks_names = {}
    for track in tracks:
        try:
            artist = track.find_element(By.CSS_SELECTOR, "p[class='truncate text-sm text-gray-500']").text
            #print(artist)

            track_name = track.find_element(By.CSS_SELECTOR, "h6[class='truncate font-medium']").text
            #print(track_name)

            tracks_names[artist] = track_name

        except selenium.common.exceptions.NoSuchElementException as NSEE:
            print(NSEE)

    return tracks_names

def create_playlist(playlist_name):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=USER_ID,
                                                   scope='playlist-modify-private',
                                                   client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://localhost:8888/callback'))

    # Создание плейлиста
    playlist = sp.user_playlist_create(user=USER_ID, name=playlist_name, public=False,
                                       description="playlist_description")

    print("Плейлист успешно создан!")
    return playlist


def add_track_to_playlist(playlist_name, tracks):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=USER_ID,
                                                   scope='playlist-modify-private',
                                                   client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://localhost:8888/callback'))

    playlists = sp.user_playlists(USER_ID, limit=100, offset=40)
    #print(playlists)
    print(len(playlists['items']))
    for playlist in playlists['items']:
        print(playlist['name'])


    #input()

    playlists = []
    offset = 0
    while True:
        results = sp.user_playlists(USER_ID, offset=offset)
        playlists.extend(results['items'])
        offset += len(results['items'])
        if not results['next']:
            break

    # Поиск плейлиста с заданным названием
    for playlist in playlists:
        print(playlist['name'])
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']

    print(len(playlists))
    #input(playlist_id)

    # Поиск плейлиста с заданным названием
    # for playlist in playlists['items']:
    #     if playlist['name'] == playlist_name:
    #         playlist_id = playlist['id']

    playlist_id = '3q5MaCtFYhTN1jwWhcmVCd'
    #Добавление треков в плейлист
    if tracks:
        track_uris = [track['uri'] for track in tracks]
        for track_uri in track_uris:
            print(track_uri)
            try:
                sp.playlist_add_items(playlist_id=playlist_id, items=[track_uri])
                print("OK!")

            except requests.exceptions.HTTPError as HTTPE:
                print(HTTPE)

            except spotipy.exceptions.SpotifyException as SE:
                print(SE)

            time.sleep(0.5)



def get_track_uri(artist_name, track_name):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=USER_ID,
                                                   scope='playlist-modify-private',
                                                   client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://localhost:8888/callback'))

    # Поиск трека
    results = sp.search(q='track:' + track_name + ' artist:' + artist_name, type='track')

    # Получение уникального идентификатора (URI) первого найденного трека
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        print(track_uri)
        return track_uri
    else:
        print("Трек не найден.")
        return None

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




def create_playlist_old(name_playlist):

    """curl --request POST \
  --url https://api.spotify.com/v1/users/31rt6qoweuvgbbo7navyuhsnzhii/playlists \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z' \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "New Playlist 1111111111",
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

    request_body = json.dumps({
        "name": "Indie bands like Franz Ferdinand but using Python",
        "description": "My first programmatic playlist, yooo!",
        "public": False  # let's keep it between us - for now
    })

    request_body = json.dumps({
        "name": "Indie bands like Franz Ferdinand but using Python",
        "description": "My first programmatic playlist, yooo!",
        "public": False  # let's keep it between us - for now
    })

    response = requests.post(url=url, data=request_body, headers={"Content-Type": "application/json",
                                                                           "Authorization": f"Bearer {token}"})

    print(response.json())

if "__main__" in __name__:
    # url = input("Url maroofy: ")
    #name_playlist = input('Playlist name: ')
    #
    # create_playlist(name_playlist)
    #
    # dict_tracks = get_playlist_from_url(url)
    #
    # tracks = []
    # for k, v in dict_tracks.items():
    #     uri = get_track_uri(k, v)
    #
    #     if uri:
    #         tracks.append({'uri': f'spotify:track:{uri}'})


    print(len(tracks))
    add_track_to_playlist(name_playlist, tracks)






    # tracks = [
    #     {'uri': 'spotify:track:4SD0V2HMxkBupk6ml9alm4'},  # URI первого трека
    #     {'uri': 'spotify:track:2RzZMPIZIEomnQDq4eYIaW'}  # URI второго трека
    # ]

