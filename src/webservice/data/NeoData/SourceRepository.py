from py2neo import rest, neo4j, cypher
from NeoRepository import NeoRepository
from entities.CoreEntities import Source


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
        return self.UpdateSource(source)

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
        SET e.title = '{2}', e.readership = {3}, e.pagerate = {4} \
        RETURN e".format(1, source.id, source.title, source.readership, source.pageRate)
        graph = self.GetGraphDb()
        results = cypher.execute(graph, query)
        return self.GetSingleEntityFromNeoResult(results, self.GetSourceFromDataRec)

    def DeleteSource(self, sourceId):
        queryHasDocs = "START n=node:sources('id:{0}') MATCH n-[:PUBLISHED]->(d) RETURN d LIMIT 1".format(sourceId)
        graph = self.GetGraphDb()
        results = cypher.execute(graph, graph)
        if results[0].count() > 0:
            #mark as hidden
            print("hide")
        else:
            #delete record
            print("delete")

__author__ = 'funhead'
