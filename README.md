# PlayMusic2Spotify
Scripts to export playlists from Google Play Music and Recreate them in spotify using An unofficial api for Google Play Music and Spotipy (Python library for the Spotify Web API)

Fisrt run the get_all_plsts_GPM.py file to download all relevent attributes of each song  and save it as a csv file for each playlist you have on Google play music

Then go to Spotify for Developers and create an app to get your Client ID and Key. Place this in the code of make_plsts_on_spotify.py

Then run make_plsts_on_spotify.py to open each of those playlist files and recreate the playlists on spotify,.
