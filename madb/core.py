from __future__ import with_statement
from madb.common.audio import Artist, Album, Song
import lxml.etree as et
import sys
import csv


class MoleculAudioDB(object):

    def __init__(self):
        self.albums = []
        self.artists = []
        self.songs = []

    def create_artists_if_not_exists(self, title):
        for artist in self.artists:
            if title == artist.title:
                return artist
        artist = Artist(title)
        self.artists.append(artist)
        return artist

    def create_album_if_not_exists(self, title, year, genre):
        for album in self.albums:
            if title == album.title and year == album.year and genre == album.genre:
                return album
        album = Album(title, year, genre)
        self.albums.append(album)
        return album

    def create_song_if_not_exists(self, title, duration, artists, album):
        for song in self.songs:
            if title == song.title and duration == song.duration and artists == song.artists and album == song.album:
                return song
        song = Song(title, duration, artists, album)
        self.songs.append(song)
        return song

    def read_from_csv(self, file):
        with open(file, 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            line_num = 0
            for record in csv_data:
                line_num += 1
                try:
                    title, duration, artists, albums, year, genre = record
                    artist_list = artists.split(';')
                    artist_objects = [self.create_artists_if_not_exists(artist) for artist in artist_list]
                    album_object = self.create_album_if_not_exists(albums, year, genre)
                    album_object.add_artists(artist_objects)
                    song_object = self.create_song_if_not_exists(title, duration, artist_objects, album_object)
                    album_object.add_song(song_object)
                    for artist_object in artist_objects:
                        artist_object.add_album(album_object)
                        artist_object.add_song(song_object)
                except ValueError, e:
                    print >> sys.stderr, "Unable to process record from %s on line %s: %s" % (file, line_num, str(e))

    def read_from_xml(self, file):
        xml_data = et.parse(file)
        for record in xml_data.getroot():
            if record.tag == "song":
                title = record.attrib['title']
                duration = record.attrib['duration']
                artist_objects = []
                album_object = None
                for child in record:
                    if child.tag == "artist":
                        artist = child.attrib['title']
                        artist_objects.append(self.create_artists_if_not_exists(artist))
                    elif child.tag == "album":
                        album = child.attrib['title']
                        year = child.attrib['year']
                        genre = child.attrib['genre']
                        album_object = self.create_album_if_not_exists(album, year, genre)
                song_object = self.create_song_if_not_exists(title, duration, artist_objects, album_object)
                album_object.add_song(song_object)
                for artist_object in artist_objects:
                    artist_object.add_album(album_object)
                    artist_object.add_song(song_object)

    def write_to_csv(self, file):
        with open(file, 'wb') as csv_file:
            csv_data = csv.writer(csv_file)
            for song in self.songs:
                record = [
                    song.title,
                    song.duration,
                    ';'.join(artist.title for artist in song.artists),
                    song.album.title,
                    song.album.year,
                    song.album.genre
                ]
                csv_data.writerow(record)

    def write_to_xml(self, file):
        root_element = et.Element('data')
        for song in self.songs:
            song_element = et.SubElement(root_element, 'song')
            song_element.set('title', song.title.decode('utf-8'))
            song_element.set('duration', str(song.duration))
            for artist in song.artists:
                artist_element = et.SubElement(song_element, 'artist')
                artist_element.set('title', artist.title.decode('utf-8'))
            album_element = et.SubElement(song_element, 'album')
            album_element.set('title', song.album.title.decode('utf-8'))
            album_element.set('year', song.album.year)
            album_element.set('genre', song.album.genre)
        with open(file, 'wb') as xml_file:
            xml_file.write(et.tostring(root_element, pretty_print=True))

    def get_stats(self):
        print "Artists:", len(self.artists)
        print "Albums:", len(self.albums)
        print "Songs:", len(self.songs)

        duration = sum([song.duration for song in self.songs])
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)

        print "Total Duration:", "%d:%02d:%02d" % (h, m, s)

    def get_song_by_title(self, title):
        for song in self.songs:
            if song.title == title:
                return song

    def get_songs_by_artist(self, title):
        for artist in self.artists:
            if artist.title == title:
                return artist.songs

    def get_songs_by_album(self, title):
        for album in self.albums:
            if album.title == title:
                return album.songs

    def get_album_by_title(self, title):
        for album in self.albums:
            if album.title == title:
                return album

    def get_albums_by_genre(self, genre):
        result = []
        for album in self.albums:
            if album.genre == genre:
                result.append(album)
        return result

    def get_album_by_song(self, title):
        for song in self.songs:
            if song.title == title:
                return song.album

    def get_albums_by_artist(self, title):
        for artist in self.artists:
            if artist.title == title:
                return artist.albums

    def get_artist_by_title(self, title):
        for artist in self.artists:
            if artist.title == title:
                return artist

    def get_artists_by_album(self, title):
        for album in self.albums:
            if album.title == title:
                return album.artists

    def get_artists_by_song(self, title):
        for song in self.songs:
            if song.title == title:
                return song.artists