import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius as genius

SPOTIFY_CLIENT_ID = 'cb988d2a4c7c4409aa077596eead42b4'
SPOTIFY_CLIENT_SECRET = 'd8eff5cdd2164cf5adc415a8ce198313'
SOUNDCLOUD_URL = 'https://soundcloud.com'
SOUNDCLOUD_SEARCH_URL = 'https://soundcloud.com/search?q={}'
artworks = 'https://i1.sndcdn.com/artworks-'
GENIUS_TOKEN = 'BF_5GVO5sHZnYAficrrnbdNtV4a8mU7cskyag4e9TyssyZ_OgDd72wypnpwzNgWH'

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

        return result[0]

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
        query = self.artist + ' ' + self.song
        try:
            results = spotify.search(q=query, type='artist,track')
            spotify_url = results['tracks']['items'][0]['album']['external_urls']['spotify']
        except:
            spotify_url = 'not found!'
        return spotify_url

    def get_image_url(self):
        data = genius.search_song(self.song, self.artist)
        return data.song_art_image_url


class Genius:

    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

    def get_lyrics(self):
        data = genius.search_song(self.song, self.artist)
        return data.lyrics
