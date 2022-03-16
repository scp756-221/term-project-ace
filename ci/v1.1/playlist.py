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

