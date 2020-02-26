import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Set the username
username = 'YOUR_USERNAME'
scope = 'user-read-private user-read-playback-state user-modify-playback-state' #for playing tracks

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username) # add scope

# Creating spotipy object
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()

#user is a dict so we have to convert it to a json variable
print(json.dumps(user, sort_keys=True, indent=4))

name = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print(f">>> Welcome to Spotipy {name}")
    print(f"You have {followers} followers")
    print()
    print("0 - search for an artist")
    print("1 - search for a song")
    print("2 - exit")

    choice = input("Your choice: ")

    if choice == "0":
        print()
        searchQuery = input("Ok, whats their name?")
        print()

        #Get search results  #search(q, limit=10, offset=0, type='track', market=None)
        searchResults = spotifyObject.search(searchQuery,1,0, "artist")
        print(json.dumps(searchResults, sort_keys=True, indent=4))

        #Artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print("Genres: ")
        for genre in artist['genres']:
            print(genre)
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']
        #Album and track details
        trackURIs = []
        trackArt = []
        z = 0 # just an incrementer

        #Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items'] # look at this var's json

        for item in albumResults:
            print("Album" + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID) # params - albumid, limit=50, offset=0
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ". " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()

        # See album art
        # while True:
        #     songSelection = input("Enter a song numer to see the album art associated with it (x to quit)")
        #     if songSelection == "x":
        #         break
        #     webbrowser.open(trackArt[int(songSelection)])

        while True:
            song = input("Enter a song number you'd like to play (x to quit)")
            if song == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIs[int(song)])
            devices = spotifyObject.devices()
            print(json.dumps(devices, sort_keys=True, indent=4))
            deviceID = devices['devices'][0]['id']
            spotifyObject.start_playback(deviceID, None, trackSelectionList)
            #webbrowser.open(trackURIs[int(song)])
            webbrowser.open(trackArt[int(song)])

    #Ending the program
    if choice == "1":
        searchQuery = input("Who do you want me to play? \n")
        #Get search results  #search(q, limit=10, offset=0, type='track', market=None)
        searchResults = spotifyObject.search(searchQuery,1,0, "track")
        #print(json.dumps(searchResults, sort_keys=True, indent=4))

        track = searchResults['tracks']['items'][0]
        print(json.dumps(track, indent = 4))
        print()

        uri = track['uri']
        print(uri)

        devices = spotifyObject.devices()
        deviceID = devices['devices'][0]['id'] # here's your spotify desktop app
        uris_list = [uri]
        spotifyObject.start_playback(deviceID, None, uris_list)

    if choice == "2":
        break
