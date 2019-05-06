#####################################################################
#	Title:	Read Playlist files and find recreate them on Spotify	#
#	Author:	Rohan Dahiya											#
#	Date:	4th May 2019											#
#####################################################################
import spotipy 
import spotipy.util
import sys
import glob
import csv
#try:
#	mode=sys.argv[1] #'auto--proper-match-only' OR 'auto--liberal' OR 'semi-auto'
#except:
#	mode='auto--proper-match-only'

#print("non-Ascii charecter support check (utf-8 encoding) --- гелик")

user='xxxx'
cliId='xxxx' # CREATE AN APP ON SPOTIFY FOR DEVs AND ADD YOUR USERNAME, API ID AND KEY HERE
cliSc='xxxx'


def authenticate():
	sp=spotipy.Spotify(spotipy.util.prompt_for_user_token(
		user,
		client_id=cliId,
		client_secret=cliSc,
		scope='playlist-modify-private',
		redirect_uri='http://google.com/'))
	return sp
#print(sp.me())

def getupto1000(q,t,sp):  #returns a list of 1000 results for a search query q of type t
	off=0
	try:
		res=sp.search(q=q,type=t,limit=50,offset=off)
	except:
		sp=authenticate()
		res=sp.search(q=q,type=t,limit=50,offset=off)
	list_res=(res[t+'s']['items'])
	while(res[t+'s']['next']!=None and off<950):
		off=off+50
		try:
			res=sp.search(q=q,type=t,limit=50,offset=off)
		except:
			sp=authenticate()
			res=sp.search(q=q,type=t,limit=50,offset=off)
		list_res=list_res+res[t+'s']['items']
	return list_res

def getSpotifySongIdsFromCSVPlaylist(Playlist,sp): # "Playlist" argument= path/name of csv file containing songs of a certain playlist
	songs_list=[]
	with open(Playlist,'r', encoding='utf-8') as f:
			songs_list=list(csv.reader(f))
			f.close()
	if songs_list==[]:
		print("FILE EMPTY---------------")
		return []
	songs_found=[]
	no_matches=0
	multiple_matches=0
	exact_match=0
	counter=0
	for song in songs_list:
		counter +=1
		print("\r#"+str(counter))
		#print("\nSONGS FOUND IN THIS PLAYLIST SO FAR:"+str(len(songs_found)))
		#print("==============Finding a match for:\n\t\""+song[1]+"\" by \""+song[0]+"\"")
		try:
			res_sngs=getupto1000(q=song[1],t='track',sp=sp) #results when searching for tracks by song name
			res_albms=getupto1000(q=song[2],t='album',sp=sp) #results when searching for albums by album name
			res_artsts=[getupto1000(q=i,t='artist',sp=sp) for i in song[0].split(' & ')] #results when searching for artists by artist name
		except:
			print("EXCEPTION:No match for: \""+song[1]+"\"\t FROM \""+song[2]+"\"\t BY \""+song[0])
			sp=authenticate()
			continue
		#check for each song in res_sngs, if there exists a song that is from an ablum that is in res_albms,
		# .. if found then check if any artist from that is in res_artists, if so then add that song to songs_found.
		full_match=[]
		nameNalbum_match=[]
		nameNartist_match=[]
		for sng in res_sngs:
			if sng['album']['id'] in [albm['id'] for albm in res_albms]:
				nameNalbum_match.append(sng['id'])
				for sng_artst in [x['id'] for x in sng['artists']]:
					if sng_artst in [x['id'] for i in res_artsts for x in i]:
						full_match.append(sng['id'])
		#print("\nFull Match:"+str(len(full_match))+"\tAlbum Match:"+str(len(nameNalbum_match)))
		if(len(full_match)==1):
			exact_match+=1
		else:
			multiple_matches+=1
		if full_match!=[] and len(full_match)<10:
			songs_found=songs_found+full_match
			continue
		if nameNalbum_match!=[] and len(nameNalbum_match)<4:
			songs_found=songs_found+nameNalbum_match
			continue
		for sng in res_sngs:
			for sng_artst in [x['id'] for x in sng['artists']]:
				if sng_artst in [x['id'] for i in res_artsts for x in i]:
					nameNartist_match.append(sng['id'])
		#print("\nArtist Match:"+str(len(nameNartist_match)))
		if nameNartist_match!=[] and len(nameNartist_match)<4:
			songs_found=songs_found+nameNartist_match
			continue
		if res_sngs!=[] and len(res_sngs)<=2:
			songs_found=songs_found+res_sngs
			continue
		#print("No match for: \""+song[1]+"\"\t FROM \""+song[2]+"\"\t BY \""+song[0])
		multiple_matches-=1
		no_matches+=1
	return {'no_matches':no_matches,'multiple_matches':multiple_matches,'exact_match':exact_match,'res': list(set(songs_found))}

def uploadPlaylist2Spotify(playlist,songs,sp):
	try:
		plst_id=sp.user_playlist_create(user,name=playlist.split('/',1)[1]+" (IMPORTD4mGPM)",public=False)['id']
	except:
		try:
			sp=authenticate()
			plst_id=sp.user_playlist_create(user,name=playlist.split('/',1)[1],public=False)['id']
		except:
			return
	off=0
	L=len(songs)
	while(off<L):
		try:
			sp.user_playlist_add_tracks(user,plst_id,songs[off:((off+100) if (off+100)<L else L)])
		except:
			pass
		off=off+100

sp=authenticate()
playlists=[x for x in glob.glob('My playlists/**')]
for playlist in playlists:
	print("###############CURRENT PLAYLIST="+playlist.split('/',1)[1]+"###############")
	recreate = getSpotifySongIdsFromCSVPlaylist(playlist,sp)
	n=recreate['no_matches']
	e=recreate['multiple_matches']
	m=recreate['exact_match']
	songs_found=recreate['res']
	print("Total Songs in Playlist:"+str(n+e+m)+"\nExact matches found for:"+str(e)+" songs\nNo matches found for:"+str(n)+" songs")
	#with open("My ready playlists/"+playlist.split('/',1)[1], 'w', encoding='utf-8') as f:
	#	csv.writer(f).writerows(songs_found)
	#	f.close()
	#with open("My ready playlists/"+playlist.split('/',1)[1], 'r', encoding='utf-8') as f:
	#	x=list(csv.reader(f))
	#	f.close()
	#songs_found=[{'id':i} for i in x]
	uploadPlaylist2Spotify(playlist=playlist,songs=songs_found,sp=sp)
