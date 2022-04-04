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
import music


@pytest.fixture
def mserv(request, music_url, auth):
    return music.Music(music_url, auth)


@pytest.fixture
def pserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)


@pytest.fixture
def plist(request):
    # To Do
    return ('MyPlayList')


def test_create(pserv, plist):
    # Test creation of playlist
    plist_id = "plist_1"
    list_name = "test"
    play_list = [plist[0], plist[1]]
    trc, p_id = pserv.create(plist_id, list_name, play_list)
    assert trc == 200 and p_id == plist_id
