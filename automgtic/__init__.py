from urllib2 import urlopen

from oauthlib.oauth2.draft25 import WebApplicationClient
from automgtic.models import Config, session


def set_client_id(client_id):
    client_id = client_id or raw_input('Client identifier: ')
    set_config('client_id', client_id)


def authorize():
    client = get_client()
    uri = client.prepare_request_uri(
            get_config('mg_server') + '/oauth/authorize',
            redirect_uri='http://foo.example/')

    print 'Go to {0}, then paste the "?code=$CODE" $CODE part.'.format(uri)
    code = raw_input('code: ')

    token_uri = client.prepare_request_uri(
            get_config('mg_server') + '/oauth/access_token',
            code=code)

    token_request = urlopen(token_uri)
    token_response = token_request.read()

    token_data = client.parse_request_body_response(token_response)

    print 'Token data: {0}'.format(token_data)

    set_config('access_token', token_data['access_token'])


def get_client():
    client = WebApplicationClient(get_config('client_id'))
    return client


def get_config(key, default=None):
    conf = Config.query.filter(Config.key == unicode(key)).first()

    if not conf and not default:
        raise ValueError('{0} is not configured.'.format(key))
    elif not conf:
        return default
    else:
        return conf.value


def set_config(key, value, checkfirst=False):
    conf = Config.query.filter(Config.key == unicode(key)).first()

    if checkfirst:
        if conf:
            raise NameError('{0} is already set in the configuration.'.format(key))

    if conf:
        conf.value = unicode(value)
    else:
        conf = Config(unicode(key), unicode(value))
        session.add(conf)

    session.commit()
