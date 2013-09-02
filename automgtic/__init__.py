import logging
import os
import hashlib
import json

from urllib2 import urlopen, Request

from poster.streaminghttp import register_openers
from poster.encode import multipart_encode
from oauthlib.oauth2 import WebApplicationClient
from configobj import ConfigObj
from validate import Validator

from automgtic.models import Media, session

register_openers()

_log = logging.getLogger(__name__)

config = app_config = mg_config = {}


def load_config():
    global config, app_config, mg_config

    configspec = ConfigObj('automgtic/config_spec.ini',
            list_values=False,
            _inspec=True)

    if os.path.exists('automgtic_local.ini'):
        config_path = 'automgtic_local.ini'
    else:
        config_path = 'automgtic.ini'

    config = ConfigObj(config_path,
            configspec=configspec,
            interpolation='ConfigParser')

    validator = Validator()
    # TODO: Add validation error handling
    validation_result = config.validate(validator, preserve_errors=True)

    app_config = config['automgtic']
    mg_config = config['mediagoblin']


load_config()

_log.debug(config)


def walk_files(directory):
    for root, directories, files in os.walk(directory):
        for f in files:
            path = os.path.join(root, f)

            if not os.path.isfile(path):
                continue

            file_extension = os.path.splitext(path)[-1][1:]
            _log.debug('file extension: {0}'.format(file_extension))

            if file_extension and \
                    file_extension.lower() in app_config.get('file_extensions'):
                yield path


def upload_if_not_exist(path, digest):
    media = Media.query.filter(Media.digest == unicode(digest)).first()

    if media:
        _log.info('Contents of {0} already exist on the server as {1}'.format(
            path,
            media.name))
        return

    _log.info('Uploading {0}...'.format(path))
    fields = {
            'file': open(path, 'rb'),
            'title': os.path.split(path)[-1],
            'description': '',
            'license': app_config['license'],
            'tags': ''}

    datagen, headers = multipart_encode(fields)

    request = Request(mg_config['server'] + '/api/submit?access_token=' \
            + mg_config['access_token'],
            datagen, headers)

    response = urlopen(request).read()
    _log.info('Posted {0}'.format(path))
    _log.debug('response: {0}'.format(response))

    media_data = json.loads(response)
    _log.debug('media data: {0}'.format(media_data))

    media = Media(digest, os.path.split(path)[-1], json.dumps(media_data))

    session.add(media)
    session.commit()


def run_autoupload(directory):
    for path in walk_files(directory):
        digest = digest_file(path)
        _log.debug('{0} - sum: {1}'.format(
            path,
            digest))
        upload_if_not_exist(path, digest)


def digest_file(f, block_size=2 ** 20):
    md5 = hashlib.md5()

    if type(f) in [str, unicode]:
        f = open(f, 'rb')

    while True:
        block = f.read(block_size)

        if not block:
            break

        md5.update(block)

    return md5.hexdigest()


def authorize():
    client = get_client()
    uri = client.prepare_request_uri(
            mg_config['server'] + '/oauth/authorize',
            redirect_uri='http://foo.example/')

    print 'Go to {0}, then paste the $CODE part in "?code=$CODE" below.'.format(uri)
    code = raw_input('code: ')

    token_uri = client.prepare_request_uri(
            mg_config['server'] + '/oauth/access_token',
            code=code)

    token_request = urlopen(token_uri)
    token_response = token_request.read()

    token_data = client.parse_request_body_response(token_response)

    print 'Token data: {0}'.format(token_data)

    mg_config['access_token'] = token_data['access_token']
    config.write()


def get_client():
    client = WebApplicationClient(mg_config['client_id'])
    return client
