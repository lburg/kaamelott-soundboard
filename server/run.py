import json
import os.path
import urllib.parse

from flask import abort
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request


app = Flask(__name__)


ROOT_URL = 'http://kaamelott-soundboard.2ec0b4.fr'


@app.route('/oembed', methods=['GET'])
def oembed():
    url = request.args.get('url')
    format_ = request.args.get('format')

    if format_ != 'json':
        abort(501)
    if not url:
        abort(404)

    sound_name = url.rsplit('/', 1)[-1]
    filepath = f'sounds/{sound_name}.mp3'

    if not os.path.exists(filepath):
        abort(404)

    static_url = f'{ROOT_URL}/{filepath}'
    content = json.dumps({
        'version': '1.0',
        'title': '',
        'url': '',
        'provider_name': '',

        'type': 'photo',
        "url": "http://farm4.static.flickr.com/3123/2341623661_7c99f48bbf_m.jpg",
        'html': f'<audio controls><source src="{static_url}" type="audio/mpeg"></audio>',
        'width': 10,
        'height': 10,
    }).encode('utf-8')
    response = make_response(content)
    response.mimetype = 'application/json'
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    quoted_url = urllib.parse.quote(request.base_url, encoding='utf-8')
    return render_template('index.html.j2', oembed_url=f'{ROOT_URL}/oembed?format=json&url={quoted_url}')
