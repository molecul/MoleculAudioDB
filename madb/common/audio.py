class Artist(object):

    def __init__(self, title):
        self.title = title
        self.albums = []
        self.songs = []

    def add_album(self, album):
        if isinstance(album, Album):
            if album not in self.albums:
                self.albums.append(album)
                album.add_artists(self)
                for song in album.songs:
                    if song not in self.songs:
                        self.songs.append(song)
                        song.add_artists(self)

    def add_song(self, song):
        if isinstance(song, Song):
            if song not in self.songs:
                self.songs.append(song)
                song.add_artists(self)

    def get_songs(self):
        return self.songs

    def get_song(self, title):
        for song in self.songs:
            if song.title == title:
                return song

    def __repr__(self):
        return self.title


class Album(object):

    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre
        self.artists = []
        self.songs = []

    def add_artists(self, artists):
        if isinstance(artists, list):
            for artist in artists:
                if artist not in self.artists:
                    self.artists.append(artist)
                    artist.add_album(self)
        elif isinstance(artists, Artist):
            if artists not in self.artists:
                self.artists.append(artists)
                artists.add_album(self)

    def add_song(self, song):
        if isinstance(song, Song):
            if song not in self.songs:
                self.songs.append(song)

    def get_songs(self):
        return self.songs

    def get_song(self, title):
        for song in self.songs:
            if song.title == title:
                return song

    def get_artists(self):
        return self.artists

    def __repr__(self):
        return "%s : [%s] : %s" % (self.title, ", ".join([str(artist) for artist in self.artists]), len(self.songs))


class Song(object):

    def __init__(self, title, duration, artists, album):
        self.title = title
        self.duration = int(duration)
        self.artists = artists
        self.album = album

    def add_artists(self, artists):
        if isinstance(artists, list):
            for artist in artists:
                if artist not in self.artists:
                    self.artists.append(artist)
                    artist.add_song(self)
        elif isinstance(artists, Artist):
            if artists not in self.artists:
                self.artists.append(artists)
                artists.add_song(self)

    def get_artists(self):
        return self.artists

    def get_album(self):
        return self.album

    def get_duration(self):
        m, s = divmod(self.duration, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s) if h > 0 else "%02d:%02d" % (m, s)

    def __repr__(self):
        return "%s - %s [%s]" % (", ".join([str(artist) for artist in self.artists]), self.title, self.get_duration())