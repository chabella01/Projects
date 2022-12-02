import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = '', 
client_secret= '',
redirect_uri='http://localhost:8888/', 
scope='user-top-read playlist-modify-public user-library-read'))



def enum_top_tracks():
    

    results = sp.current_user_top_tracks(
        time_range='short_term'
        )['items'] #Save user's top songs from short term (4 weeks)
    tracks = [x['uri'] for x in results] #save top song uri's into array
    
    return tracks

def get_avg_keymode(trackarr):

    features = sp.audio_features(trackarr) #takes in top tracks and generates audio features of each song into array

    t = {'valence': [], 'mode': [], 'danceability': [], 'energy': []} #dictionary of desired quality amounts
    
    for el in features: #parse through features and append desired values into dictionay
        t['valence'].append(el['valence'])
        t['mode'].append(el['mode'])
        t['danceability'].append(el['danceability'])
        t['energy'].append(el['energy'])
    
    #take averages of maximums of the desired feature values
    vavg = round(sum(t['valence']) / float(len(t['valence'])), 4)
    mt = max(set(t['mode']), key=t['mode'].count)
    davg  = round((sum(t['danceability']) / float(len(t['danceability']))), 4)
    eavg = round(sum(t['energy']) / float(len(t['energy'])), 4)
    return [vavg, mt, davg, eavg] #return array of values
    
    
def search(clist, t): #takes in list of feature vales and list of top tracks
    
    #input top tracks and feature values with a range of randomness to generate similar music recomendations
    recomms = sp.recommendations(
        seed_tracks = t[0:4], 
        target_valence = round(random.uniform(clist[0] - 0.1, clist[0] + 0.1), 4), 
        target_mode = clist[1], 
        target_danceability = round(random.uniform(clist[2] - 0.2, clist[2] + 0.2), 4), 
        target_energy = round(random.uniform(clist[3] - 0.2, clist[3] + 0.2), 4), 
        target_popularity = int(random.uniform(0, 10))
        )
    re = []
    for el in recomms['tracks']: #create list of recommended song uri's 
        re.append(el['uri'])

    return re

def create_playlist(tracks): #takes in recommended song uri's
    user_id = sp.me()['id']
    name = input('Name your playlist!: ') #ask user to name their generated playlist
    #create playlist with a given playlist description
    sp.user_playlist_create(
        user=user_id, 
        name=name, 
        public=True, 
        description='A playlist based on your recent listening habits. Hope you enjoy :)'
        )
    #find created playlist within library, then fill it with recommended tracks!!!
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
