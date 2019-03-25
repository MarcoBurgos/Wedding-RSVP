import pprint
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import json


#check added

def get_tracks():

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    uri = 'spotify:user:marcoburgos:playlist:0hDMbPox24ra5hgXwvCnGR'
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]

    results = sp.user_playlist(username, playlist_id)
    results = json.dumps(results)
    json_output = json.loads(results)
    # #write elements
    # json_file = open("playlist.json", "w")
    # json_file.write(json.dumps(json_output["tracks"]["items"], indent=4))

    tracks=[]
    tracks_on_playlist = json_output["tracks"]["items"]
    for track in tracks_on_playlist:
        song_name = track["track"]["name"]
        artist_name = track["track"]["artists"][0]["name"]
        album_img = track["track"]["album"]["images"][0]["url"]
        track_preview = track["track"]["preview_url"]
        track_info = {"song_name":song_name, "artist_name": artist_name,
                    "album_img": album_img, "track_preview": track_preview}
        tracks.append(track_info)

    return tracks
