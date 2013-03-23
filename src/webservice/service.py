import re
import cherrypy
from data.NeoData.DocumentRepository import DocumentRepository
from data.NeoData.SourceRepository import SourceRepository
import simplejson as json

class Resource(object):
    def __init__(self, repository):
        self.repository = repository

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, id=-1):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        if id < 1:
            return self.repository.GetItems()
        else:
            return self.repository.GetItem(id)

    def OPTIONS(self):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.status = 200
        return "OK"

    def PUT(self, id=-1):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        rawbody = cherrypy.request.body.read()
        body = json.loads(rawbody)
        self.repository.SetItem(body)

    def to_html(self):
        html_item = lambda(name, value): '<div>{name}:{value}</div>'.format(**vars())
        items = map(html_item, self.content.items())
        items = ''.join(items)
        return '<html>{items}</html>'.format(**vars())

    @staticmethod
    def from_html(data):
        pattern = re.compile(r'<div\>(?P<name>.*?)\:(?P<value>.*?)\</div\>')
        items = [match.groups() for match in pattern.finditer(data)]
        return dict(items)


class ResourceIndex(Resource):
    def to_html(self):
        html_item = lambda (name, value): '<div><a href="{value}">{name}</a></div>'.format(**vars())
        items = map(html_item, self.content.items())
        items = ''.join(items)
        return '<html>{items}</html>'.format(**vars())


class Root(object):
    pass


root = Root()

root.document = Resource(DocumentRepository())
root.source = Resource(SourceRepository())
#root.sidewinder = Resource({'color': 'red', 'weight': 176, 'type': 'stable'})
#root.teebird = Resource({'color': 'green', 'weight': 173, 'type': 'overstable'})
#root.blowfly = Resource({'color': 'purple', 'weight': 169, 'type': 'putter'})
#root.resource_index = ResourceIndex({'sidewinder': 'sidewinder', 'teebird': 'teebird', 'blowfly': 'blowfly'})

conf = {
    'global': {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8081,
    },
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    }
}

cherrypy.quickstart(root, '/', conf)
