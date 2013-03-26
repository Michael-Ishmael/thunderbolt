from py2neo import rest, neo4j, cypher


class NeoRepository(object):
    def __init__(self, refNodeId, refRelName, entityIndex):
        self.uri = "http://localhost:7474/db/data/"
        self.refNodeId = refNodeId
        self.refRelName = refRelName
        self.entityIndex = entityIndex

    def GetGraphDb(self):
        return neo4j.GraphDatabaseService(self.uri)

    def GetAllEntitiesQuery(self):
        query = "START rn=node:references('id:{0}') MATCH (rn)-[:{1}]->(e) RETURN e"\
            .format(str(self.refNodeId), self.refRelName)
        return query

    def GetEntityQuery(self, entityId):
        query = "START e=node:{0}('id:{1}') RETURN e"\
            .format(str(self.entityIndex), entityId)
        return query

    def CreateEntityQuery(self, entity):
        query = "START rn=node:references('id:{0}') CREATE UNIQUE (rn)-[:{1}]->(e) RETURN e" \
            .format(str(self.refNodeId), self.refRelName)
        return query

    def GetAllEntities(self):
        query = self.GetAllEntitiesQuery()
        neoResult = cypher.execute(self.GetGraphDb(), query)
        return self.GetEntityCollectionFromNeoResult(neoResult)

    def GetEntity(self, entityId):
        query = self.GetEntityQuery(entityId)
        neoResult = cypher.execute(self.GetGraphDb(), query)
        return self.GetSingleEntityFromNeoResult(neoResult)

    def CreateEntity(self, entity):
        query = self.CreateEntityQuery(entity)
        neoResult = cypher.execute(self.GetGraphDb(), query)
        return self.GetSingleEntityFromNeoResult(neoResult)


    def GetEntityCollectionFromNeoResult(self, neoResult):
        items = []
        for result in neoResult[0]:
            item = result[0].get_properties()
            items.append(item)
        return items

    def GetSingleEntityFromNeoResult(self, neoResult):
        items = self.GetEntityCollectionFromNeoResult(neoResult)
        if len(items) > 0:
            return items[0]
        return None



__author__ = 'funhead'
