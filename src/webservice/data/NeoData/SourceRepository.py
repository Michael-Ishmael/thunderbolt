from py2neo import rest, neo4j, cypher
from NeoRepository import NeoRepository
from entities.Document import Source


class SourceRepository(NeoRepository):
    def __init__(self):
        super(SourceRepository, self).__init__(1, "SOURCE")

    def GetItems(self):
        m = lambda (d): d.__dict__
        return map(m, self.GetAllSources())

    def GetItem(self, itemId):
        return self.GetSource(itemId).__dict__

    def SetItem(self, dict):
        source = Source()
        source.__dict__.update(dict)
        self.UpdateSource(source)

    def GetAllSources(self):
        query = self.GetAllEntitiesQuery()
        graph = self.GetGraphDb()
        results = cypher.execute(graph, query)
        return self.GetEntityCollectionFromNeoResult(results, self.GetSourceFromDataRec)

    def GetSource(self, sourceId):
        query = self.GetEntityQuery(sourceId)
        graph = self.GetGraphDb()
        results = cypher.execute(graph, query)
        docs = []
        return self.GetSingleEntityFromNeoResult(results, self.GetSourceFromDataRec)

    def GetSourceFromDataRec(self, rec):
        source = Source()
        source.id = rec["id"]
        source.title = rec["title"]
        source.readership = rec["readership"]
        source.pageRate = rec["pagerate"]
        return source

    def UpdateSource(self, source):
        query = "START rn=node:references('id:{0}') MATCH (rn)-[:SOURCE]->(e) WHERE e.id = {1} \
        SET n.title = '{2}', n.readership = {3}, n.pagerate = {4} \
        RETURN n".format(1, source.id, source.title, source.readership, source.pageRate)
        graph = self.GetGraphDb()
        results = cypher.execute(graph, query)
        return self.GetSingleEntityFromNeoResult(results, self.GetSourceFromDataRec)

__author__ = 'funhead'
