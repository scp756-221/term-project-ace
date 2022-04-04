"""
Test the *_original_artist routines.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import playlist
<<<<<<< Updated upstream
=======
import music


@pytest.fixture
def mserv(request, music_url, auth):
    return music.Music(music_url, auth)
>>>>>>> Stashed changes


@pytest.fixture
def pserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)


@pytest.fixture
def plist(request):
    # To Do
<<<<<<< Updated upstream
    return None

=======
    return ('MyPlayList')
>>>>>>> Stashed changes

def test_create(pserv, plist):
    # Test creation of playlist
    plist_id = "plist_1"
    list_name = "test"
    play_list = [plist[0], plist[1]]
    trc, p_id = pserv.create(plist_id, list_name, play_list)
    assert trc == 200 and p_id == plist_id
