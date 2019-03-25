import pprint
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import json

if len(sys.argv) > 3:
    username = sys.argv[1]
    playlist_id = sys.argv[2]
    track_ids = sys.argv[3:]
else:
    print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
    sys.exit()
scope = 'playlist-modify-public playlist-modify-private'
token = util.prompt_for_user_token(username, scope,)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    print(results)
else:
    print("Can't get token for", username)

# ============================

# python add_songs.py HlBXWbjNQ8iHIN1ue7xZ6Q 0hDMbPox24ra5hgXwvCnGR 4IAi2FpLcsFTZOPISZv1ng
