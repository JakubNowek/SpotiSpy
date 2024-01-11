import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import json
from jsondiff import diff


def get_followed_artist_list(sp, limit=50) -> dict:
    artist_list = []
    results = sp.current_user_followed_artists(limit=limit)['artists']
    artist_list.extend(results['items'])
    while results['next']:
        results = sp.next(results)['artists']
        artist_list.extend(results['items'])

    # for artist in artist_list:
    #     print(artist['name'], artist['id'])
    return artist_list


def get_artist_albums(sp, artist_id, album_type=('album', 'single'), limit=50) -> dict:
    albums = []
    for type in album_type:
        results = sp.artist_albums(artist_id, album_type=type, limit=limit)
        #print(results['total'])
        albums.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])

    # for album in albums:
    #     print(album['name'], album['id'])
    return albums


def get_album_tracks(sp, album_id, limit=50) -> dict:
    tracks = []
    results = sp.album_tracks(album_id=album_id, limit=limit)
    #print(results['total'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    #
    # for track in tracks:
    #     print('     ', track['name'], track['id'])
    return tracks


def get_artists_discography(sp, artist_id) -> dict:
    artists_tracks = []
    artist_albums = get_artist_albums(sp, artist_id=artist_id)
    for album in artist_albums:
        #print(album['name'], album['total_tracks'])
        artists_tracks.extend(get_album_tracks(sp, album['id']))
    # print(len(artists_tracks))
    return artists_tracks


def artist_tracks_to_add(sp, artist_id) -> list:
    list_of_tracks_id_to_add = []
    artist_discography = get_artists_discography(sp, artist_id=artist_id)

    for track in artist_discography:
        list_of_tracks_id_to_add.append(track['id'])

    return list_of_tracks_id_to_add


def export_spotify_dict_to_json_format(spotify_json_object, list_name: str, list_of_key_tuples: list[tuple[str, str]]):
    """
    :param spotify_json_object: iterable object - spotify json object
    :param list_name: name of the main list in json, containing dictionaries
    :param list_of_key_tuples: list of tuples containing dictionaries' keys (key in json dict, key in spotify json)
    """
    main_json = {list_name: []}
    dict_as_list_item = {}
    for item in spotify_json_object:
        for key_tuple in list_of_key_tuples:
            dict_as_list_item[key_tuple[0]] = item[key_tuple[1]]
        main_json[list_name].append(dict_as_list_item)
        dict_as_list_item = {}
    #print(main_json)
    return main_json


def export_json_to_file(json_dict: dict[str:list[dict]], filename: str):
    """
    :param json_dict: dict containing a list of dicts
    :param filename: name of the destination file
    """

    # Serializing json
    json_object_to_export = json.dumps(json_dict, indent=4)

    # Writing to sample.json
    with open(filename, "w") as outfile:
        outfile.write(json_object_to_export)


def read_data_from_json(filename: str, list_name: str):
    json_file = open(filename, "r")
    json_data = json.load(json_file)
    json_file.close()
    list_from_main_json = json_data[list_name]
    return list_from_main_json


# def tracks_id_to_add_creator(sp, artists_id_list):
#     list_of_tracks_id_to_add = []
#     for artist_id in artists_id_list:
#         list_of_tracks_id_to_add.extend(artist_tracks_to_add(sp, artist_id))
#
#     return list_of_tracks_id_to_add


# ta funkcja jest w sumie na razie bez sensu bo ma tyle argumentów co wywołanie i tyle
# def add_tracks_to_playlist(sp, tracks_id_list, playlist_id):
#     sp.playlist_add_items(playlist_id=playlist_id, items=tracks_id_list)

# setting the scopes to authorize
scope = 'user-follow-read \
        user-library-read \
        user-top-read \
        playlist-modify-public \
        playlist-modify-private \
        user-read-private \
        user-read-email'

# client credentials
cid = '69cb1a2b53aa409ebbf168afe0bd4b02'
secret = '84a4ef954c3b4327af66350a76496d04'
username = 'yt2fz80w9y0gxc49640wbxeub'
artist_to_add_list = [['Chef Lay', '6xQoqRtTEYNZNF5gUMG3iu', 590],
['CHOPPA TEE', '12iGnI7m6kxA8LpEQ1xdiJ', 91],
['Ash Bash Tha Rapper', '4GHSsO2bndtYIfy8js9hUN', 370],
['LeeLee Babii', '4sq5z4vRwCaR9tYr4lhvYj', 416],
['Liddy Mechelle', '6wvAw2O489yb5baR7jDxKT', 588],
['Aporshianta', '3hDxk4BmL68RMkEHGV4mBI', 327],
['Stephanie Palomares', '1IvMHLX4QynHiuSVikYoP2', 113],
['Jeane Marie', '3yP7Ekj2BVXARVv7nvcU6r', 350],
['Mia lourde', '0vJ7ktn9hZt6T0vqBLNF1R', 80],
['Stvr Baby', '2BxIP27i38uM4Ds5Pbdk3h', 191],
['Sharondaduhdon', '38nZfbBg9YbejAt4Zzzy6Y', 270],
['Leyla Blue', '6HpIVA13SPof8sYuXRUfxj', 538],
['Bri Trilla', '0bUkjDAvq74Ppu5rSp1SN8', 52],
['Mrz. Showbizz', '5Pj95JbfrrIQJMbJLKJsVk', 468],
['Tinkaabellaaa', '6yB3T4NveoMCbzGupoPkvd', 591],
['Five2blasian', '5Mnet43StJMpH4Jc12tdwa', 465],
['Quality Bunny', '1JkHWrIYwyJVtwMtNObLze', 115],
['Lala2muchhh', '7BXwzjTdFNOc6ZrxQk0at8', 610],
['Mala', '4s2QCd13TEb6gTkPLIX9w4', 415],
['Daisy', '290RgPy7mVNjeiCVY33yC3', 189],
['Natasia', '3PsRFlJ0Lf94lNET6VGZSm', 306],
['Dee Duchess', '45y9bdytJiHdKwu3Ug6Etj', 359],
['Pussy Riot', '2hThsqaVEAWhWPBXnaOfB9', 231],
['Auntie Piggy', '6hkSisAwJkzQ3UkCqjz976', 568],
['Lavish Caminshion', '0TCsN3TDu9ZL5b54hQzz93', 35],
['Kae Kajora', '4FZs29EztyuuQknNJ7oUT9', 369],
['NajaMillion', '4xjFbnIaXePGFfYFe7xd1R', 424],
['Big Indo', '6S6ITvCmnsccK8Sdv8vqL1', 551],
['Princess Bre', '1V2oxBGVXw1JwZTvr03YVJ', 135],
['Kayla B', '5yvTe64rt7c77FUaskqaCZ', 517],
['Bbyafricka', '019gRg7DezPMbaI1xRZD6W', 1],
['Nija', '7f9KxQWD88MZrSY6jc0zoW', 633],
['ItsCourtney!', '0bZovW36bYttxuwptidwIL', 53],
['Heavy Baile', '2E4sNJOOy9hae0J8DkT43M', 194],
['chriseanrock', '3Idu5nTg2S3wrYwVkPqiwa', 291],
['Reneé Rapp', '2hUYKu1x0UZQXvzCmggvSn', 232],
['Stony', '1gfXNiyfLEKouLvNPmrvLk', 157],
['BriBiase', '4tNro16CgwzfDfLK9YgFDl', 418],
['TRINA', '7hLQp9nd2WwuSd9urqu3pJ', 639],
['Reina Reign', '4b1OYOIVOk5MHhq9fJft8A', 394],
['Shawna & Mia', '1IbE7R5bQCSBeMhVRbWnU7', 112],
['Intuwiish', '0MH4kp4bzWFsx0OBWh5GwV', 25],
['Supa Cindy', '22e8seQKsb34z8dW26bG5P', 184],
['Nikki Jayy', '4MONW063BePUr0702vTw6c', 379],
['Coco Bliss', '2oXb6vq3maLjFiFWLL5MpA', 245],
['Notorious Bxtch', '0RF7Kx0y6KgNNAAdoGzRXJ', 31],
['A. Chic', '09bs0SLPQ7Mjfsg2Rom6MO', 10],
['Golden Ego', '5zBPlMAiHtUs5zLjkW3b6F', 518],
['Front Paije', '5t0Y1ulwuavBxJqxI3CMrl', 510],
['Misshy Money', '2SY1HckMjuERyoLAkb2x8D', 212],
['Marlé Blu', '36Tyg8d0rbi8HTVyynvA7s', 266],
['Lil Reeka', '2eZ44pc86sB6o1qU4xW4Qe', 226],
['Big Boss Blossom', '6QvbxO1OIuWVxVS2SH9Rrg', 549],
['Emony Keelen', '5zLaDcImyXoOM2DQMmEyoU', 520],
['MONI DA G', '4twqXMj5X9jIGTAwrZLwYI', 420],
['Peaches Adaba', '1AVlRnmtTppAMrm96iEfJu', 99],
['Bunny Liiu', '6vEgaRuQU3vD4ae9SrL7tR', 585]]

target_playlist_id = '6UDrcXzV1goOZldp8nOZum'
auth_manager = SpotifyOAuth(username=username,
                            scope=scope,
                            client_id=cid,
                            client_secret=secret,
                            redirect_uri='http://localhost:3000')

sp = spotipy.Spotify(auth_manager=auth_manager)


followed_artist_list = get_followed_artist_list(sp)
#print(followed_artist_list)
""" Load old list of artists"""
old_list = read_data_from_json('old_list_of_artists.json', 'artists')

""" Generate new list of followed artists and transform it into json format"""
json_to_export = export_spotify_dict_to_json_format(followed_artist_list, "artists",
                                                    [("artist_name", "name"), ("artist_id", "id")])
new_list = json_to_export["artists"]

#new_list = read_data_from_json('new_list_of_artists.json', 'artists')


new_added_artists_list = [x for x in new_list if x not in old_list]  # czyli wszystko co się pojawiło nowe
artists_deleted_from_old_list = [x for x in old_list if x not in new_list]  # czyli wszystko co było usunięte z nowym

print('What is new: ', new_added_artists_list)
print('What has been deleted: ', artists_deleted_from_old_list)

""" In case of any failure save new_added_artists_list and artists_deleted_from_old_list to json file """

last_added_json_format = {"artists": new_added_artists_list}
last_deleted_json_format = {"artists": artists_deleted_from_old_list}

export_json_to_file(last_added_json_format, "last_added_artists.json")
export_json_to_file(last_deleted_json_format, "last_deleted_artists.json")


#TODO jak skoncze kombinowac to trzeba zmienic nazwe pliku na old zeby sie nadpisywalo

export_json_to_file(json_to_export, "new_list_of_artists.json")

""" Add all new songs to playlist"""
for artist in new_added_artists_list:
    sp.playlist_add_items(playlist_id=target_playlist_id, items=artist_tracks_to_add(sp, artist["artist_id"]))


# TODO maksymalnie 1 request może dodać 100 utworów więc trzeba podzielić to jeszcze





# #
# # # Serializing json
# # json_object = json.dumps(json_to_export, indent=4)
# #
# # # Writing to sample.json
# # with open("old_list_of_artists.json", "w") as outfile:
# #     outfile.write(json_object)
#
# # artist_database = {"artists": []}
# # artist_data = {}
# # for artist in followed_artist_list[:3]:
# #     artist_data["artist_name"] = artist['name']
# #     artist_data["artist_id"] = artist['id']
# #     artist_database["artists"].append(artist_data)
# #     artist_data = {}
# # print(artist_database)
#
# # { "artists": [
# #     {"artist_name": "Chef Lay", "artist_id": "6xQoqRtTEYNZNF5gUMG3iu", "artist_index": 590},
# #     {"artist_name": "CHOPPA TEE", "artist_id": "12iGnI7m6kxA8LpEQ1xdiJ", "artist_index": 91},
# #     {"artist_name": "Ash Bash Tha Rapper", "artist_id": "4GHSsO2bndtYIfy8js9hUN", "artist_index": 370}
# #     ]
# # }
# # artist_albums = get_artist_albums(sp, artist_id='0hCNtLu0JehylgoiP8L4Gh')
#
#
# # album_tracks = get_album_tracks(sp,'4Rh57STD18rbjXbBrx2X65')
#
#
# # artist_discography = get_artists_discography(sp, artist_id='6vEgaRuQU3vD4ae9SrL7tR')
#
#
# ###### sp.playlist_add_items(playlist_id='6UDrcXzV1goOZldp8nOZum', items=to_add)

#
#
#
# # print(sp.current_user())  # print userinfo
# # sp.user_playlist_create(username, 'TestSpotispy', public=True, collaborative=False, description="Test playlist for SpotiSpy")
