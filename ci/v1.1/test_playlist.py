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
def pserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)

@pytest.fixture
def plist(request):
    return ('MyPlayList')


def test_update(pserv, mserv):
    origin_list_name = ' what is love '
    new_list_name = ' what is IBMer '
    trc1, p_id = pserv.create(origin_list_name)
    assert trc1 == 200
    trc2 = pserv.update_playlist_listname(p_id, new_list_name)
    assert trc2 == 200
    trc3, listname, list = pserv.read(p_id)
    assert trc3 == 200 and listname == new_list_name and list == []
