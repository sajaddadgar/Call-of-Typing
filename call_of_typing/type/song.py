import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from call_of_typing.call_of_typing.secrets import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius as genius

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET))
genius = genius.Genius(GENIUS_TOKEN)


class SoundCloud:

    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

    def get_songs_list(self):
        result = []
        search_content = self.artist + ' ' + self.song
        response = requests.get(SOUNDCLOUD_SEARCH_URL.format(quote_plus(search_content)))
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a'):
            data = {}
            if link.parent.name == 'h2':
                data['title'] = link.text
                data['url'] = SOUNDCLOUD_URL + link['href']
                result.append(data)

        return result

    def get_song_image(self, url):
        script = []
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')
        for inner in soup.find_all('script'):
            script.append(inner)
        data = str(script[len(script) - 1])
        result = data[data.index(artworks):]
        image_url = result.split('"')[0]
        return image_url


class Spotify:

    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

    def get_duration_ms(self):
        query = self.artist + ' ' + self.song
        results = spotify.search(q=query, type='artist,track')
        return results['tracks']['items'][0]['duration_ms']

    def get_song_url(self):
        # todo: get url from spotify api not genius api
        data = genius.search_song(self.song, self.artist)
        try:
            spotify_url = data.media[1]['url']
        except:
            spotify_url = False
        return spotify_url

    def get_image_url(self):
        data = genius.search_song(self.song, self.artist)
        return data.song_art_image_url





class Genius:

    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

    def get_lyric(self):
        data = genius.search_song(self.song, self.artist)
        return data.lyrics


s = Genius('alan walker', 'faded')
print(s.get_lyric())