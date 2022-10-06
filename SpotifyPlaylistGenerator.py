import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = '', 
client_secret= '',
redirect_uri='http://localhost:8888/', 
scope='user-top-read playlist-modify-public user-library-read'))



def enum_top_tracks():
    tracks = []
    artists = []
    results = sp.current_user_top_tracks(time_range='short_term')
    for idx, item in enumerate(results['items']):
        track = item['uri']
        tracks.append(track)
        artists.append(item['artists'][0]['id'])
    return [tracks, artists]

def get_avg_keymode(trackarr):

    features = sp.audio_features(trackarr[0])

    t = {'valence': [], 'mode': [], 'danceability': [], 'energy': []}
    for el in features:
        t['valence'].append(el['valence'])
        t['mode'].append(el['mode'])
        t['danceability'].append(el['danceability'])
        t['energy'].append(el['energy'])
    
    vavg = float('%.4f' % (sum(t['valence']) / len(t['valence'])))
    mt = max(set(t['mode']), key=t['mode'].count)
    davg  = float('%.4f' % (sum(t['danceability']) / len(t['danceability'])))
    eavg = float('%.4f' % (sum(t['energy']) / len(t['energy'])))
    return [vavg, mt, davg, eavg]

def search(clist, t):
    tr = t[0]
    ar = t[1]
    
    recomms = sp.recommendations(seed_tracks=tr[0:5], target_valence= random.uniform(clist[0] - 0.1, clist[0] + 0.1), target_mode= clist[1], 
    target_danceability= random.uniform(clist[2] - 0.2, clist[2] + 0.2), 
    target_energy= random.uniform(clist[3] - 0.2, clist[3] + 0.2), 
    target_popularity= int(random.uniform(0, 10)))
    re = []
    for el in recomms['tracks']:
        re.append(el['uri'])

    return re

def create_playlist(tracks):
    user_id = sp.me()['id']
    name = input('Name your playlist!: ')
    sp.user_playlist_create(user=user_id, name=name, 
    public=True, description='A playlist based on your recent listening habits. Hope you enjoy :)')

    playlists = sp.user_playlists(user=user_id)['items']

    for el in playlists:
        if el['name'] == name:
            p_id = el['id']
    
    sp.user_playlist_add_tracks(user=user_id, playlist_id=p_id, tracks=tracks)



    

def main():
    t = enum_top_tracks()
    criteria = get_avg_keymode(t)
    tracks = search(criteria, t)
    create_playlist(tracks)


if __name__ == '__main__':
    main()
