import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup

BASE_URL = 'https://soundcloud.com'
SEARCH_URL = 'https://soundcloud.com/search?q={}'


class SoundCloud:

    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

    def get_songs_list(self):
        links = []
        search_content = self.artist + ' ' + self.song
        data = requests.get(SEARCH_URL.format(quote_plus(search_content)))
        soup = BeautifulSoup(data.content, 'html.parser')
        for link in soup.find_all('a'):
            if link.parent.name == 'h2':
                links.append(BASE_URL + link['href'])
        return links

    def get_song_image(self, url):
        script = []
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')
        for inner in soup.find_all('script'):
            script.append(inner)
        data = str(script[len(script) - 1])
        result = data[data.index('https://i1.sndcdn.com/artworks-'):]
        image_url = result.split('"')[0]
        return image_url
