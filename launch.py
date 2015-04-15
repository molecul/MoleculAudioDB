from madb import MoleculAudioDB

mdb = MoleculAudioDB()
mdb.read_from_csv('example_data/madb.csv')
#mdb.read_from_xml('example_data/madb.xml')
#mdb.write_to_csv('madb.csv')
#mdb.write_to_xml('madb.xml')
mdb.get_stats()

albums = mdb.get_albums_by_genre('Instrumental')
print ", ".join([str(album) for album in albums])

artists = mdb.get_artists_by_song('Forest Maiden')
print ", ".join([str(artist) for artist in artists])

song = mdb.get_song_by_title('Forest Maiden')
print song