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
# import music


@pytest.fixture
def pserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)


@pytest.fixture
def plist(request):
    # To Do

    return ('MyPlayList')


def test_simple_run(pserv, mserv):
    # Test creation of playlist
    song1 = ('k. d. lang',  'Hallelujah')
    song2 = ('Kris',  'Bad girl')
    trc1, m_id1 = mserv.create(song1[0], song1[1])
    trc2, m_id2 = mserv.create(song2[0], song1[1])
    # plist_id = "plist_1"
    list_name = "mylist"
    play_list = [m_id1, m_id2]
    trc, p_id = pserv.create(list_name, play_list)
    assert trc == 200
