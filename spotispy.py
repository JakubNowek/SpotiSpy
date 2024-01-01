import spotipy
import spotipy.util as util

scope = 'user-follow-read'
cid = '69cb1a2b53aa409ebbf168afe0bd4b02'
secret = '84a4ef954c3b4327af66350a76496d04'

token = util.prompt_for_user_token(username='69cb1a2b53aa409ebbf168afe0bd4b02', scope=scope, client_id=cid, client_secret=secret, redirect_uri='http://localhost:3000')

if token:
    sp = spotipy.Spotify(auth=token)
    artists_list = sp.current_user_followed_artists(limit=3)
    print(artists_list['artists']['items'])
else:
    print("Can't get token for", username)