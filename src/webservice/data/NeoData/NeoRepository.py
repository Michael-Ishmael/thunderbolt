from py2neo import rest, neo4j, cypher


class NeoRepository(object):
    def __init__(self, refNodeId, refRelName):
        self.uri = "http://localhost:7474/db/data/"
        self.refNodeId = refNodeId
        self.refRelName = refRelName

    def GetGraphDb(self):
        return neo4j.GraphDatabaseService(self.uri)

    def GetAllEntitiesQuery(self):
        query = "START rn=node:references('id:{0}') MATCH (rn)-[:{1}]->(e) RETURN e"\
            .format(str(self.refNodeId), self.refRelName )
        return query

    def GetEntityQuery(self, entityId):
        query = "START rn=node:references('id:{0}') MATCH (rn)-[:{1}]->(e) WHERE e.id = {2} RETURN e"\
            .format(str(self.refNodeId), self.refRelName , entityId)
        return query

    def GetEntityCollectionFromNeoResult(self, neoResult, transFunc):
        items = []
        for result in neoResult[0]:
            item = transFunc(result[0])
            items.append(item)
        return items

    def GetSingleEntityFromNeoResult(self, neoResult, transFunc):
        if len(neoResult) > 0 and len(neoResult[0]) > 0 and len(neoResult[0][0]) > 0:
            return transFunc(neoResult[0][0][0])
        return None



__author__ = 'funhead'
