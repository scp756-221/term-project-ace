import requests


class Playlist():
    """Python API for the music service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
        'http://cmpt756s2:30001/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def read(self, p_id):
        # read a play list by id
        r = requests.get(
            self._url + p_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None

        plist = r.json()['Items'][0]
        return r.status_code, plist['ListName'], plist['PlayList']

    def delete(self, p_id):
        requests.delete(
            self._url + p_id,
            headers={'Authorization': self._auth}
        )

    def create(self, list_name, play_list=[]):
        """Create an artist, song pair.

        Parameters
        ----------
        artist: string
            The artist performing song.
        song: string
            The name of the song.
        orig_artist: string or None
            The name of the original performer of this song.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Music.
            The string is the UUID of this song in the music database.
        """

        payload = {'ListName': list_name,
                   'PlayList': play_list}
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['play_list_id']

    def write_music_to_playlist(self, music_add, p_id):
        """Write the original artist performing a song.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        orig_artist: string
            The original artist performing the song.

        Returns
        -------
        number
            The HTTP status code returned by the music service.
        """
        r = requests.put(
            self._url + 'write_music_to_playlist/' + p_id,
            json={'MusicAdd': music_add},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def update_playlist_listname(self, p_id, list_name):
        """Create an artist, song pair.

        Parameters
        ----------
        artist: string
            The artist performing song.
        song: string
            The name of the song.
        orig_artist: string or None
            The name of the original performer of this song.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Music.
            The string is the UUID of this song in the music database.
        """
        r = requests.put(
            self._url + 'write_music_to_playlist/' + p_id,
            json={'ListName': list_name},
            headers={'Authorization': self._auth}
        )

        if r.status_code != 200:
            return r.status_code, None

        return r.status_code
