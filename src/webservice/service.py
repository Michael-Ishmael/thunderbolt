import re
import cherrypy
from data.NeoData.NeoRepository import NeoRepository
from data.NeoData.DocumentRepository import DocumentRepository
from data.NeoData.SourceRepository import SourceRepository
import simplejson

class Resource(object):
    def __init__(self, repository):
        self.repository = repository

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, id=-1):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        if id < 1:
            return self.repository.GetAllEntities()
        else:
            return self.repository.GetEntity(id)

    def OPTIONS(self):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.status = 200
        return "OK"

    def PUT(self, id=-1):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        rawbody = cherrypy.request.body.read()
        return self.set_item(rawbody)

    def set_item(self, json):
        item = simplejson.loads(json)
        return self.repository.SetItem(item)

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


class GenericResource(Resource):
    def __init__(self, repository):
        super(GenericResource, self).__init__(repository)

    @cherrypy.tools.json_out()
    def GET(self, index, id):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        entities = self.repository.GetEntitiesForIndex(index, id)

if __name__ == "__main__":

    class Root(object):
        pass


    root = Root()

    docRepo = NeoRepository(2, "DOCUMENT", "documents")
    root.document = Resource(docRepo)
    sourceRepo = NeoRepository(1, "SOURCE", "sources")
    root.source = Resource(sourceRepo)
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
    cherrypy.server.stop()
    cherrypy.quickstart(root, '/', conf)

