#!/usr/local/bin/python3.6
import string
import os
import cherrypy
from feed2pod import feed2pod

FEEDPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))


def sanitize_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    return filename


def authorized(token):
    if not authorized.token:
        with open('TOKEN', 'r') as f:
            authorized.token = f.read().strip()
    return token == authorized.token
authorized.token = None


class Root(object):
    @cherrypy.expose
    def index(self):
        files = ['<li><a href="feeds/{0}">{0}</a></li>'.format(f) for f in os.listdir(FEEDPATH) if f.endswith('.xml')]
        return 'Files:<ul>' + '\n'.join(files) + '</ul>'

    @cherrypy.expose
    def refresh(self, feed=None, token=None):
        if not authorized(token):
            raise cherrypy.HTTPError(401, 'Unauthorized')
        out = ["REFRESHING: {}".format(feed)]
        rss = feed2pod(feed)
        if rss:
            filename = 'feed-' + sanitize_filename(feed) + '.xml'
            with open(os.path.join(FEEDPATH, filename), 'w') as f:
                f.write(rss)
                out.append('Created: {}'.format(filename))
        else:
            out.append('...failed')
        return '<br>'.join(out)


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    #'log.access_file': 'access.log',
    #'log.error_file': 'error.log',
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 28119,
})
cherrypy.quickstart(Root(), '/', {
    '/feeds': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': FEEDPATH,
    }
})

