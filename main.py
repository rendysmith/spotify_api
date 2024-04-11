import requests
import json
import tempfile

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

scope_private = 'playlist-modify-private'
scope_public = 'playlist-modify-public'

def get_all_playlist(name_playlist):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=USER_ID,
                                                   scope='playlist-modify-private',
                                                   client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://localhost:8888/callback'))

    # Создание плейлиста
    playlists = sp.user_playlists(USER_ID)
    #print(playlists)

    for playlist in playlists['items']:
        print(playlist['name'], playlist['id'])
        if name_playlist == playlist['name']:
            return playlist['id']

    return False


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
                                                   scope='playlist-modify-public',
                                                   client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://localhost:8888/callback'))

    # Создание плейлиста
    playlist = sp.user_playlist_create(user=USER_ID,
                                       name=playlist_name,
                                       public=True,
                                       description="playlist_description")

    print("Плейлист успешно создан!")
    return playlist


def add_track_to_playlist(playlist_id, tracks):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=USER_ID,
                                                   scope=scope_public,
                                                   client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://localhost:8888/callback'))

    #Добавление треков в плейлист
    if tracks:
        track_uris = [track['uri'] for track in tracks]
        for track_uri in track_uris:
            print(track_uri)
            try:
                sp.playlist_add_items(playlist_id=playlist_id, items=[track_uri])
                print("OK!")

            except requests.exceptions.HTTPError as HTTPE:
                print('ERROR HTTPE:', HTTPE)

            except spotipy.exceptions.SpotifyException as SE:
                print('ERROR SE:', SE)

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
    url = input("Url maroofy: ")
    name_playlist = input('Playlist name: ')
    filename = f"{name_playlist}.txt"

    while True:
        id_playlist = get_all_playlist(name_playlist)

        if id_playlist == False:
            create_playlist(name_playlist)

        else:
            break

    #id_playlist = input('Playlist ID: ')
    dict_tracks = get_playlist_from_url(url)
    print(dict_tracks)
    input()

    tracks = []
    for k, v in dict_tracks.items():
        if k.isascii() and v.isascii():
            uri = get_track_uri(k, v)

            if uri:
                tracks.append({'uri': f'{uri}'})

    with open(filename, 'w') as file:
        json.dump(tracks, file)

    print("Список сохранен в файле", filename)
    input()


    #id_playlist = '7sCbGOYY5W84YggFBICPel'
    #tracks = [{'uri': 'spotify:track:4UwKxnuowew8lKCajgfCOf'}, {'uri': 'spotify:track:37WQvgYTZCMV5jgZZSAVPJ'}, {'uri': 'spotify:track:3Q3UcMK3bgNeWT4hM2mnwp'}, {'uri': 'spotify:track:6kxXgUyPMsP43mbXAMVjWY'}, {'uri': 'spotify:track:1phg6Fi9WsvIRsDMWvJ23d'}, {'uri': 'spotify:track:0SoPHQiKza3LPsdRQcUPsV'}, {'uri': 'spotify:track:7E12QRk94o3DBLzkySXFqn'}, {'uri': 'spotify:track:3fVuFRW7bzsb2izAFfW1fY'}, {'uri': 'spotify:track:5U42kA5FXpVUTip2848aCy'}, {'uri': 'spotify:track:7CPQjjMEUJp8w0Pke3WOB4'}, {'uri': 'spotify:track:61cy6pfxZd55Ab10uUMaHA'}, {'uri': 'spotify:track:2oQ9wp3ox6kXh9RN6hpYBO'}, {'uri': 'spotify:track:1VTCvUpkg1LoOiBMNXruUO'}, {'uri': 'spotify:track:2K4OpcgDTv4lxDggSe392w'}, {'uri': 'spotify:track:3HkJmYJo1TSCUbOOkRg4vH'}, {'uri': 'spotify:track:38qc60ogMKm7pGgv2jhN6Y'}, {'uri': 'spotify:track:4qkeCliBAGQp5v1EkNKfnB'}, {'uri': 'spotify:track:3h6nYgcXiCiM610kS2zmtg'}, {'uri': 'spotify:track:6KKi8AlNHSEnyKnGfuLpJK'}, {'uri': 'spotify:track:1gFF3FyAFhVi5a5zg71hAa'}, {'uri': 'spotify:track:0OozTFnYguoBdF1D2k1feu'}, {'uri': 'spotify:track:5HCe3Nv0xW8zKM9ytD0r3w'}, {'uri': 'spotify:track:5hQOTzeC43CQU3Ocje3S0s'}, {'uri': 'spotify:track:7rGsD4fuZqfYav8vLV52dk'}, {'uri': 'spotify:track:3ESMC7No32nIqN5LTttpMa'}, {'uri': 'spotify:track:0TWsl2of40gpU3yVQIKkZ3'}, {'uri': 'spotify:track:2pVc2nNQBtgEsP2NXu4dlu'}, {'uri': 'spotify:track:6uclpa0K9glSyx2FCCm4IH'}, {'uri': 'spotify:track:00e4BROWmM8Vn9XsajGF8A'}, {'uri': 'spotify:track:03Oa1b16EQl6Wc0aAv3FbT'}, {'uri': 'spotify:track:0eFDvgee43HDh5sA92Zbmu'}, {'uri': 'spotify:track:2bnmm9j3fsebVJ8WUA95Ir'}, {'uri': 'spotify:track:3y5THSBSyzNQCQOwfatPG8'}, {'uri': 'spotify:track:5PNUWUQnO4sdH871xp7PPk'}, {'uri': 'spotify:track:668efL1ezo70OCg9RmomUO'}, {'uri': 'spotify:track:72VdhczObnJAEJggQFQQrY'}, {'uri': 'spotify:track:0QMxj5QTJ9fARjdyR1IYBP'}, {'uri': 'spotify:track:0juz17xpIkhkM9vs9fL02M'}, {'uri': 'spotify:track:09sgNdH5WG89FiIGuoxU0K'}, {'uri': 'spotify:track:7G2Pqxm5vqYfveLOLb2eA6'}, {'uri': 'spotify:track:4ulUMToiQi1fuBeF42MQbc'}, {'uri': 'spotify:track:1LHzBlklRm3FHAa6etl8kM'}, {'uri': 'spotify:track:0pHjK2MtdrDozQaiLvxJxQ'}, {'uri': 'spotify:track:7DwJdDsnEh8fkDOfdjv1IW'}, {'uri': 'spotify:track:7LH7mscd4DbfNPiyyTupo2'}, {'uri': 'spotify:track:2u8t8R3mErJVWFmdOoajql'}, {'uri': 'spotify:track:6n3f0aunEl2NEZDNIXsGk6'}, {'uri': 'spotify:track:0HSNyqqLRPc5DrSU2J2p9j'}, {'uri': 'spotify:track:2aypHFkSxFLFKNNli1FraI'}, {'uri': 'spotify:track:4NYtCHzcWwA9JZgUJraVtq'}, {'uri': 'spotify:track:75ka750qIdgisBq7FWa1UU'}, {'uri': 'spotify:track:2Y7iqlT7RVVVUpoJb7kRP6'}, {'uri': 'spotify:track:7EOfFZyIdQIBPduG43TQNd'}, {'uri': 'spotify:track:5uTyCmj7sKlRk361li3wIE'}, {'uri': 'spotify:track:5IJlO0suinkRbpOxBlnW1l'}, {'uri': 'spotify:track:5ljLoKEK5HK5Gvdi8FeM00'}, {'uri': 'spotify:track:4wh6nUIOy434H1noeLG29G'}, {'uri': 'spotify:track:5lvGmYmIT5zvGLGXUE4z7W'}, {'uri': 'spotify:track:1ODJndLkQhSGqrqWdvs81A'}, {'uri': 'spotify:track:1KjNtGQpxGE2bdNI9nPl11'}, {'uri': 'spotify:track:6ARRN8sfajHcNTHdoLujXt'}, {'uri': 'spotify:track:4mJJcl2mum9clyHByw9m2R'}, {'uri': 'spotify:track:7qdQzUjOpvfCPN6cNB79G4'}, {'uri': 'spotify:track:2I1lJIr4MnzsoIghb3vc0V'}, {'uri': 'spotify:track:1bPaEmlsj9pUUpwujyZ8NQ'}, {'uri': 'spotify:track:4i2zjXVsyXny8YQNbXfPX1'}, {'uri': 'spotify:track:1fxlrLGVv8AG5nvhAPIoCi'}, {'uri': 'spotify:track:65Yf13Si6vea8sHZlEQy1M'}, {'uri': 'spotify:track:3vdRsq76cfSYQTLQh7WpNa'}, {'uri': 'spotify:track:3BFkPJem7gkabGNweUGBFG'}, {'uri': 'spotify:track:3W4DMKzECWFadd5zmlKKIA'}, {'uri': 'spotify:track:4XBY5RJXMnUonjBQioQmYu'}, {'uri': 'spotify:track:2kPN9284vzcNYf1nFenYLl'}, {'uri': 'spotify:track:14kQfm6jxRsxDzqqV08cq6'}, {'uri': 'spotify:track:6kVAQA6jc6rgFO1YZ3oXxm'}, {'uri': 'spotify:track:684jYvOxfaoaoQulnucHf7'}, {'uri': 'spotify:track:3YddzDMvNjhvJu4rCSyaAB'}, {'uri': 'spotify:track:054m8sghASM7Bwnb8kYrg3'}, {'uri': 'spotify:track:22yQFzulK2B5LEjad7gC4M'}, {'uri': 'spotify:track:0xerSbsQ6QdQQ9EnfN4EfK'}, {'uri': 'spotify:track:2fhf1maDG8NrWtIZc5Tw2I'}, {'uri': 'spotify:track:44ctMpSHjWkxOezwOMw3lq'}, {'uri': 'spotify:track:1JSi9HMdvXZXJ273KAFgBr'}, {'uri': 'spotify:track:75lbM3Im3VAK3d9j6nBBbT'}, {'uri': 'spotify:track:1kN4yaZWPIB9KnKgu6zKD6'}, {'uri': 'spotify:track:1rosV8WunHKdFbeHMb6fa4'}, {'uri': 'spotify:track:5DLGAQGRGP033z4ZTPOEX3'}, {'uri': 'spotify:track:0SSIu4CcGITHdatDmjlA6H'}, {'uri': 'spotify:track:5TCpJxq3QRO1COGxYDg50l'}, {'uri': 'spotify:track:1Z2hUgpvX3Qc6ZEnzsnabK'}, {'uri': 'spotify:track:4W4pQeDiuRon21h02QM7Gs'}, {'uri': 'spotify:track:6UnhpCsFyhC24rFYRLswor'}, {'uri': 'spotify:track:3H6x81DBMYVpIL6OtbKRKx'}, {'uri': 'spotify:track:7hAcCQAdtxl9EH2XDcL1PE'}, {'uri': 'spotify:track:1JojpXL8uxxSzUczn3zXu3'}, {'uri': 'spotify:track:2VS2AUrd9c4V114SDZwloa'}, {'uri': 'spotify:track:5ju1OW6cmrbU81SPjGsBVH'}, {'uri': 'spotify:track:0lYgP84iATAqwCx3L5NNcU'}, {'uri': 'spotify:track:00Qc7BnEe7GvpGlrZTVUip'}, {'uri': 'spotify:track:3mHQPwHDd8kac6w1sQWxCg'}, {'uri': 'spotify:track:5tGZNDzrvP59BLqoQHorRc'}, {'uri': 'spotify:track:6nAOPf2oucGq09jx2XietA'}, {'uri': 'spotify:track:3cRdTUKiOfpH6okvv6PsZC'}, {'uri': 'spotify:track:207dSv39thVLXqxORLSMu4'}, {'uri': 'spotify:track:1F9LgyVBd3OiZIfpXkFPsV'}, {'uri': 'spotify:track:06O6Nqhf3M8G00fyYLwAPD'}, {'uri': 'spotify:track:24OaFYNv9eN7gcRNiAPDqT'}, {'uri': 'spotify:track:0dLB4JGw0E79hs8oKqxxJV'}, {'uri': 'spotify:track:38hLWF8eP7YTURvbGLztiH'}, {'uri': 'spotify:track:2aRhnrpL6QsPGdmfSqhdLR'}, {'uri': 'spotify:track:0fhxIOyAoCQIqxFKjZKLqs'}, {'uri': 'spotify:track:0OaMX8DjDNQF3bWUK0WWDv'}, {'uri': 'spotify:track:2tUBfeR7yQch0hYjWNe9Kw'}, {'uri': 'spotify:track:27e5Wgv7tCIXWOPJ4Bi0Mp'}, {'uri': 'spotify:track:565iY5E0qxDyqZV4zvJapn'}, {'uri': 'spotify:track:6YGJyqmC0NbZ5KRMYOFqWT'}, {'uri': 'spotify:track:1uUzDP5Q4AaFX01C5NTGB0'}, {'uri': 'spotify:track:5hbnX8jLADwDS1U2rq5hB9'}, {'uri': 'spotify:track:4kte3OcW800TPvOVgrLLj8'}, {'uri': 'spotify:track:09MwA1oKdqwKeG08nl3gCY'}, {'uri': 'spotify:track:7CUcDE7u1cAJKWgv1IWwZK'}, {'uri': 'spotify:track:5EDrgM1qXcy68djuUlifHX'}, {'uri': 'spotify:track:1ltJqhaikL0JjYB6dEgDTx'}, {'uri': 'spotify:track:7E9JskUAYjuSQ0UzlRTDih'}, {'uri': 'spotify:track:0a5naCcAMHAllb64oROc3V'}, {'uri': 'spotify:track:28790GBTiOK55Xq17zYXgA'}, {'uri': 'spotify:track:4viqoub4ZrHJq76FD0k7lX'}, {'uri': 'spotify:track:5ZTtuPgzA4Clj9khjsIOs8'}, {'uri': 'spotify:track:7iQ6dWrco8LKMdgohGUs5v'}, {'uri': 'spotify:track:7unBMV5ZHIkl9JluT5tnwW'}, {'uri': 'spotify:track:03W3HVz9cdPONnBrnpQ9JX'}, {'uri': 'spotify:track:67rMCNdR8bek7TLEj81K8L'}, {'uri': 'spotify:track:5VkzriS69iYc0gJO5I8WoK'}, {'uri': 'spotify:track:1LHFbV4IG5cdkamqlHynAl'}, {'uri': 'spotify:track:6luQVL3PAhlnLZ4ubuGxsr'}, {'uri': 'spotify:track:13I5jvb5l1wI2N4p0DFabZ'}, {'uri': 'spotify:track:3SaWiOZCUidvBsAMXEHLIb'}, {'uri': 'spotify:track:4WZiBNrn5q7gaSQ8iO9Qdn'}, {'uri': 'spotify:track:02rHn2RVpfTmGuy6TtqDIU'}, {'uri': 'spotify:track:15e4hRmLL3tHcMSbB3UPXT'}, {'uri': 'spotify:track:1GPZJ2YgzLOSSI9e3MahT7'}, {'uri': 'spotify:track:07uNVEUqmvpUt95aadULFy'}, {'uri': 'spotify:track:04BccJPx60wkU01um5W2jz'}, {'uri': 'spotify:track:01W3aCG1QGSkhtr1ZUqBwM'}, {'uri': 'spotify:track:4A3r7gGR7ZquccTjkr2ZBM'}, {'uri': 'spotify:track:6CSj7d6w71LbKwZxFnmhBO'}, {'uri': 'spotify:track:0x7IWLYUMASzoaod1XWhFr'}, {'uri': 'spotify:track:4ZlhWZeyVZ55DF03niYA58'}, {'uri': 'spotify:track:399JjEfwQTgxLfJIwLdWWr'}, {'uri': 'spotify:track:7jYXDXDJCuIdaGSrGaFslp'}, {'uri': 'spotify:track:1MFmiir89nKDrfw8AjeNKu'}, {'uri': 'spotify:track:7zL9Jq5EuXRJotxDDyNQiu'}, {'uri': 'spotify:track:0lwyEKZ1cygPfVRh5XR7ZO'}, {'uri': 'spotify:track:05Ir9ADgavsIvJpiva3qXt'}, {'uri': 'spotify:track:2nYdWGLtKTIFkbCcgSvwKE'}, {'uri': 'spotify:track:0ZUN0INihFQFlicgidV8cK'}, {'uri': 'spotify:track:3cLy4pyWXzQVIDAFczHDTA'}, {'uri': 'spotify:track:4XBNtgnopNho8FCWz293P3'}, {'uri': 'spotify:track:7rNlhuIXxTay18EiYDGnOn'}, {'uri': 'spotify:track:0KdzqY5vvgUsu8ae18hLf7'}, {'uri': 'spotify:track:5iocz7QMhDXlBJ4EAJV55i'}, {'uri': 'spotify:track:6TjJ0jylEZLX6rBGvRMZPk'}, {'uri': 'spotify:track:4au7g8u7nIjXeBERRwokcI'}, {'uri': 'spotify:track:2ah8aNKuFRLjCEzObjS43B'}, {'uri': 'spotify:track:1I0RaOzynbYw97tuqbRnEb'}, {'uri': 'spotify:track:4CKVkhTne0EM5rHDP3tj3k'}, {'uri': 'spotify:track:5La98IZObDHrEu5wLhkR47'}, {'uri': 'spotify:track:213ueJa1LSAt0yHv89bIcu'}, {'uri': 'spotify:track:3vqoFimcqPT5wCd9SSpewd'}, {'uri': 'spotify:track:2ehTCjLmqSbrMTFHuTUgSS'}, {'uri': 'spotify:track:2eGtnmd5OjwLLKV5X3u7N5'}, {'uri': 'spotify:track:1nCS1LTAdBkkQ5SyuPUzeN'}, {'uri': 'spotify:track:5smNyiaetj9MKBKWE4bcV9'}, {'uri': 'spotify:track:2UtSSLsxWYBHhi1WlSV8bz'}, {'uri': 'spotify:track:0r9FdSe7Yoz77tajgcCIAp'}, {'uri': 'spotify:track:7M8eyoZjW2z60d8qCNCYk4'}, {'uri': 'spotify:track:0ZdNCTRYCglUX2PP0cTMyo'}, {'uri': 'spotify:track:4RoL0OoChVZ2Sg693NJIdD'}, {'uri': 'spotify:track:57aiGoDr3QX5I3PrrN1Rom'}, {'uri': 'spotify:track:1POy2LK8fzc8zsrxniLQnX'}, {'uri': 'spotify:track:5FqB6fVmAcnWAhfOU55CUh'}, {'uri': 'spotify:track:27I1XsYzsHnQSnxCC1vpRo'}, {'uri': 'spotify:track:52xzfKjexL5ShkZ9sCKSSt'}, {'uri': 'spotify:track:3sk0an74u9Mwr8syvmFCpl'}, {'uri': 'spotify:track:5bMfIrZnq6rhRuOPdN4WKB'}, {'uri': 'spotify:track:1CgtKjJhSNuef3MY4q05At'}, {'uri': 'spotify:track:4bWu7hfyhlJqBnrrkw5vSX'}, {'uri': 'spotify:track:4bsKNTlsE4JtQHoyAqpnwU'}, {'uri': 'spotify:track:4gmPV7hLts2cm3vWmFMwvo'}, {'uri': 'spotify:track:4EnP2fOYJZMWkg7uxwatLf'}, {'uri': 'spotify:track:2Ew57cOS7w5A8wEWYVm3Hn'}, {'uri': 'spotify:track:0MY7fdkLoNIQfjyfEVYBfF'}, {'uri': 'spotify:track:2V9Eh93eM5UzYIgtIJirob'}, {'uri': 'spotify:track:7eIlDyCaZPDU6r3BlidRuD'}, {'uri': 'spotify:track:71XV9DcHaIuaJOnFBRfpzl'}, {'uri': 'spotify:track:5qHa4UZ42gzeCgbwgA9aX2'}, {'uri': 'spotify:track:6LVBjN5ftpSyoZiQ0XSAjl'}, {'uri': 'spotify:track:6ghONAjj9YbeBRXsbV3n9n'}, {'uri': 'spotify:track:5cwRMLkCHCdO7pQZvXEmB7'}, {'uri': 'spotify:track:49jcisYtUt9I8rMPKK5aTE'}, {'uri': 'spotify:track:7tAgm59BL2p5Gf2Z3xShFC'}, {'uri': 'spotify:track:6WXgnWECCqIyZQycb4QpBN'}, {'uri': 'spotify:track:1JdXgHlfs6BmKEKDbeICyA'}, {'uri': 'spotify:track:5yQ49nFjVUQ3I46v0lnhIs'}, {'uri': 'spotify:track:5wYE2aXk67kLXo7ElIFztn'}, {'uri': 'spotify:track:2IO2cqIR8nTqx4SgEh49Rw'}, {'uri': 'spotify:track:1BRGy09bvswQSl8XM1hjYg'}, {'uri': 'spotify:track:1GEtBIHZ1Fsr2NBKmRgmpo'}, {'uri': 'spotify:track:1GAILB8HDGbvMCxMCCtb6y'}, {'uri': 'spotify:track:7DY5HnhdoatAw9Ku3lEuiU'}, {'uri': 'spotify:track:5PuG2nuKpaInatXKVYfXhA'}]
    #tracks = [{'uri': 'spotify:track:4UwKxnuowew8lKCajgfCOf'}, {'uri': 'spotify:track:37WQvgYTZCMV5jgZZSAVPJ'},
    #print(tracks)
    #print(len(tracks))

    # id_playlist = '5SPFZ0CXBGuLTyPlvaVyL6'
    #
    # tracks = [
    #     {'uri': 'spotify:track:6Pg4tpm9tdRiN6nh17kY3Z'},
    #     {'uri': 'spotify:track:12QxawwqcosD3hxdRTSIUB'},
    #     {'uri': 'spotify:track:2ZwdmczWxLplSUi5qyrHo5'}]
    add_track_to_playlist(id_playlist, tracks)





    'https://open.spotify.com/track/4xFxK0FXmNlUDRgCaIQCVn?si=cc9e5fe04c5d4d6b'
    # tracks = [
    #     {'uri': 'spotify:track:4SD0V2HMxkBupk6ml9alm4'},  # URI первого трека
    #     {'uri': 'spotify:track:2RzZMPIZIEomnQDq4eYIaW'}  # URI второго трека
    # ]

