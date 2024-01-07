import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd


def get_followed_artist_list(sp):
    # get all followed artists list
    artist_name_id_index = []
    limit = 50
    last_artist_id = None
    number_of_items = 0
    next_item = 1
    while next_item is not None:
        artists = sp.current_user_followed_artists(limit=limit, after=last_artist_id)
        artists_list = artists['artists']['items']
        next_item = artists['artists']['next']

        for artist in artists_list:
            # print(artist['name'])
            artist_index_in_list = list(artists_list).index(artist)
            artist_name_id_index.append([artist['name'], artist['id'], artist_index_in_list + limit * number_of_items])
            last_artist_id = artist['id']
        number_of_items += 1
    return artist_name_id_index

# setting the scopes to authorize
scope = 'user-follow-read user-library-read user-top-read'

#client credentials
cid = '69cb1a2b53aa409ebbf168afe0bd4b02'
secret = '84a4ef954c3b4327af66350a76496d04'
username = '69cb1a2b53aa409ebbf168afe0bd4b02'
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

auth_manager = SpotifyOAuth(username=username,
                            scope=scope,
                            client_id=cid,
                            client_secret=secret,
                            redirect_uri='http://localhost:3000')

sp = spotipy.Spotify(auth_manager=auth_manager)

followed_artist_list = get_followed_artist_list(sp)
for artist in followed_artist_list:
    print(artist)
