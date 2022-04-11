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
    return ('MyPlayList')


def test_update(pserv):
    origin_list_name = ' what is love '
    new_list_name = ' what is IBMer '
    trc1, p_id = pserv.create(origin_list_name)
    assert trc1 == 200
    trc2 = pserv.update_playlist_listname(p_id, new_list_name)
    assert trc2 == 200
    trc3, listname, list = pserv.read(p_id)
    assert trc3 == 200 and listname == new_list_name and list == []


def test_create_list(pserv, mserv):
    song1 = ('k. d. lang',  'sun')
    song2 = ('Kris',  'Bad girl')
    song3 = ('John Lennon', 'Oh yoko')
    trc1, m_id1 = mserv.create(song1[0], song1[1])
    trc2, m_id2 = mserv.create(song2[0], song2[1])
    trc3, m_id3 = mserv.create(song3[0], song3[1])
    # plist_id = "plist_1"
    list_name = "love is what"
    play_list = [m_id1, m_id2, m_id3]
    trc, p_id = pserv.create(list_name, play_list)
    assert trc == 200


def test_delete_list(pserv):
    list_name = 'is what love'
    trc1, p_id = pserv.create(list_name)
    assert trc1 == 200
    pserv.delete(p_id)


def test_create_and_read(pserv, mserv):

    # Test creation of playlist
    song1 = ('k. d. lang',  'Hallelujah')
    song2 = ('Kris',  'Bad girl')
    trc1, m_id1 = mserv.create(song1[0], song1[1])
    trc2, m_id2 = mserv.create(song2[0], song1[1])
    # plist_id = "plist_1"
    list_name = "What is love"
    play_list = [m_id1, m_id2]
    trc, p_id = pserv.create(list_name, play_list)
    assert trc == 200
    trc3, l_name, p_list = pserv.read(p_id)
    assert trc3 == 200 and l_name == list_name and p_list == play_list
