#####################################################################
#	Title:	Read Playlist files and find recreate them on Spotify	#
#	Author:	Rohan Dahiya											#
#	Date:	28th April 2019											#
#####################################################################

from gmusicapi import Mobileclient as Mc
import csv
import os

api=Mc()
api.oauth_login(api.FROM_MAC_ADDRESS,api.perform_oauth())

lib=api.get_all_songs()
plsts=api.get_all_user_playlist_contents()
thumbs=[]
for i in lib:
	if ('rating' in i.keys()) and (i['rating']=='5'):
		thumbs.append(i)

if 'My playlists' not in os.listdir():
	os.makedirs('My playlists')

def writeP2F(P,F):
	songs=[]
	for i in P:
		songs.append([i['artist'],i['title'],i['album'],i['year']])
	csv.writer(F).writerows(songs)

print("\n\t\t...writing \"Thumbs Up\"...")
with open("My playlists/Thumbs Up",'w', encoding='utf-8') as f:
	writeP2F(thumbs,f)
	f.close()

print("\n\t\t...writing \"All Songs\" (\\\"Last Added\")...")
with open("My playlists/All Songs",'w', encoding='utf-8') as f:
	writeP2F(lib,f)
	f.close()
#print("\n\tWritten 2/"+(len(plsts)+2)+" playlists")

for plst in plsts:
	print("\n\t\t...writing \""+plst['name']+"\"...")
	tracks=[]
	for i in plst['tracks']:
		if i['source']=='2':
			tracks.append(i['track'])
	with open("My playlists/"+plst['name'], 'w', encoding='utf-8') as f:
		writeP2F(tracks,f)
		f.close()
