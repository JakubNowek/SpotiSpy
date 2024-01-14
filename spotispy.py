import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


def get_followed_artist_list(sp, limit=50) -> list[dict]:
    artist_list = []
    results = sp.current_user_followed_artists(limit=limit)['artists']
    artist_list.extend(results['items'])
    while results['next']:
        results = sp.next(results)['artists']
        artist_list.extend(results['items'])

    # for artist in artist_list:
    #     print(artist['name'], artist['id'])
    return artist_list


def get_artist_albums(sp, artist_id, album_types=('album', 'single'), limit=50) -> list[dict]:
    albums = []
    for album_type in album_types:
        results = sp.artist_albums(artist_id, album_type=album_type, limit=limit)
        #print(results['total'])
        albums.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])

    # for album in albums:
    #     print(album['name'], album['id'])
    return albums


def get_album_tracks(sp, album_id, limit=50) -> list[dict]:
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


def get_artists_discography(sp, artist_id) -> list[dict]:
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


""" Setting the scopes to authorize """
scope = 'user-follow-read \
        user-library-read \
        user-top-read \
        playlist-modify-public \
        playlist-modify-private \
        user-read-private \
        user-read-email'

""" Client credentials """


""" Load credentials from .config file """
credentials = read_data_from_json('.config', 'credentials')
cid = credentials["cid"]
secret = credentials["secret"]
username = credentials["username"]


target_playlist_id = '6UDrcXzV1goOZldp8nOZum'  # TestSpotispy
auth_manager = SpotifyOAuth(username=username,
                            scope=scope,
                            client_id=cid,
                            client_secret=secret,
                            redirect_uri='http://localhost:3000')

# sp = spotipy.Spotify(auth_manager=auth_manager)
#
#
# followed_artist_list = get_followed_artist_list(sp)
# # for artist in followed_artist_list:
# #     print(artist['name'], artist['id'])
#
# """ Load old list of artists"""
# old_list = read_data_from_json('old_list_of_artists.json', 'artists')
#
# """ Generate new list of followed artists and transform it into json format"""
# new_dict_of_artists_json_to_export = export_spotify_dict_to_json_format(followed_artist_list, "artists",
#                                                                         [("artist_name", "name"), ("artist_id", "id")])
# new_list = new_dict_of_artists_json_to_export["artists"]
#
# """ Generate difference between new and old artists lists """
# new_added_artists_list = [x for x in new_list if x not in old_list]  # czyli wszystko co się pojawiło nowe
# artists_deleted_from_old_list = [x for x in old_list if x not in new_list]  # czyli wszystko co było usunięte z nowym
#
# print('What is new: ', new_added_artists_list)
# print('What has been deleted: ', artists_deleted_from_old_list)
#
# """ In case of any failure save new_added_artists_list and artists_deleted_from_old_list to json file """
# last_added_json_format = {"artists": new_added_artists_list}
# last_deleted_json_format = {"artists": artists_deleted_from_old_list}
#
# export_json_to_file(last_added_json_format, "last_added_artists.json")
# export_json_to_file(last_deleted_json_format, "last_deleted_artists.json")
#
# print("New artists count: ", len(new_added_artists_list))
#
# """ Overwrite old list of artists with new_added_artists_list """
# export_json_to_file(new_dict_of_artists_json_to_export, "old_list_of_artists.json")
#
# """ Add all new songs to playlist artist by artist from new_added_artists_list """
# for artist in new_added_artists_list:
#     items = artist_tracks_to_add(sp, artist["artist_id"])
#     while items:
#         sp.playlist_add_items(playlist_id=target_playlist_id, items=items[:100], )
#         items = items[100:]

# # print(sp.current_user())  # print userinfo
# # sp.user_playlist_create(username, 'TestSpotispy', public=True, collaborative=False, description="Test playlist for SpotiSpy")
