import spotipy
import spotipy.util as util
import pandas as pd

# setting the scopes to authorize
scope = 'user-follow-read user-library-read user-top-read'

#client credentials
cid = '69cb1a2b53aa409ebbf168afe0bd4b02'
secret = '84a4ef954c3b4327af66350a76496d04'

# setting access token
token = util.prompt_for_user_token(username='69cb1a2b53aa409ebbf168afe0bd4b02',
                                   scope=scope,
                                   client_id=cid,
                                   client_secret=secret,
                                   redirect_uri='http://localhost:3000')

if token:
    sp = spotipy.Spotify(auth=token)

    art = []
    limit = 50
    last_artist_id = None
    number_of_items = 0
    next_item= 1
    while next_item is not None:
        artists = sp.current_user_followed_artists(limit=limit, after=last_artist_id)
        artists_list = artists['artists']['items']
        next_item = artists['artists']['next']

        for artist in artists_list:
            #print(artist['name'])
            artist_index_in_list = list(artists_list).index(artist)
            art.append([artist['name'], artist['id'], artist_index_in_list + limit * number_of_items])
            last_artist_id = artist['id']
        number_of_items+= 1

    for artist in art:
        print(artist)
else:
    print("Can't get token for", username)