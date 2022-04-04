"""
SFU CMPT 756
Sample application---playlist service.
"""

# Standard library modules
import logging
import sys
# import time

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

# import jwt

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'playlist process')

bp = Blueprint('app', __name__)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/<playlist_id>', methods=['GET'])
def get_play_list(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')

    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_play_list(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    url = db['name'] + '/' + db['endpoint'][2]
    response = requests.delete(
        url,
        params={"objtype": "playlist", "objkey": playlist_id},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<playlist_id>', methods=['PUT'])
def update_playlist_listname(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        list_name = content['ListName']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"objtype": "playlist", "ListName": list_name},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/', methods=['POST'])
def create_play_list():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        ListName = content['ListName']
        PlayList = content['PlayList']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][1]
    payload = {"objtype": "playlist",
               "ListName": ListName,
               "PlayList": PlayList}

    response = requests.post(
        url,
        json=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())

# @bp.route('/write_music_to_playlist/<playlist_id>', methods=['PUT'])
# def write_music_to_playlist(playlist_id):
#     headers = request.headers
#     # check header here
#     if 'Authorization' not in headers:
#         return Response(json.dumps({"error": "missing auth"}),
#                         status=401,
#                         mimetype='application/json')
#     try:
#         content = request.get_json()
#         music_add = content['MusicAdd']

#     except Exception:
#         return json.dumps({"message": "error reading arguments"})
#     payload = {"objtype": "playlist", "objkey": playlist_id}
#     url = db['name'] + '/' + db['endpoint'][3]
#     response = requests.put(
#         url,
#         params=payload,
#         json={"OrigArtist": orig_artist},
#         headers={'Authorization': headers['Authorization']})
#     return (response.json())


# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
