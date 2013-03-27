from py2neo import rest, neo4j, cypher


class NeoRepository(object):
    def __init__(self, refNodeId, refRelName, entityIndex):
        self.uri = "http://localhost:7474/db/data/"
        self.refNodeId = refNodeId
        self.refRelName = refRelName
        self.entityIndex = entityIndex
        self.graphDB = self.GetGraphDb()

    def GetGraphDb(self):
        return neo4j.GraphDatabaseService(self.uri)

    def GetEntitiesForIndex(self, index, filter):
        query = "START n=node:{0}('id:{1}') RETURN n" \
            .format(index, filter)
        return query

    def GetAllEntitiesQuery(self):
        query = "START rn=node:references('id:{0}') MATCH (rn)-[:{1}]->(e) RETURN e"\
            .format(str(self.refNodeId), self.refRelName)
        return query

    def GetEntityQuery(self, entityId):
        query = "START e=node:{0}('id:{1}') RETURN e"\
            .format(str(self.entityIndex), entityId)
        return query

    def GetReferenceNode(self):
        refNode = self.GetGraphDb().get_indexed_node("references", "id", str(self.refNodeId))
        return refNode

    def GetAllEntities(self):
        query = self.GetAllEntitiesQuery()
        neoResult = cypher.execute(self.GetGraphDb(), query)
        return self.GetEntityCollectionFromNeoResult(neoResult)

    def GetEntity(self, entityId):
        query = self.GetEntityQuery(entityId)
        neoResult = cypher.execute(self.GetGraphDb(), query)
        return self.GetSingleEntityFromNeoResult(neoResult)

    def GetEntityFromTitle(self, title):
        query = "start n = node:references('id:{0}') match n-[:{1}]->s where s.title =~ '(?i){2}.*' return s" \
            .format(self.refNodeId, self.refRelName,title)
        neoResult = cypher.execute(self.GetGraphDb(), query)
        return self.GetSingleEntityFromNeoResult(neoResult)

    def CreateEntity(self, entity):
        newId = self.GetNextId()
        entity["id"] = newId
        refNode = self.GetReferenceNode()
        newNode = self.graphDB.get_or_create_indexed_node(self.entityIndex, "id", str(newId), entity)
        newNode.create_relationship_from(refNode, self.refRelName)
        return newNode

    def UpdateEntity(self, entity):
        node = self.graphDB.get_indexed_node(self.entityIndex, "id", str(entity["id"]))
        if node is not None:
            node.set_properties(entity)
        return node

    def DeleteEntity(self, entityId):
        node = self.graphDB.get_indexed_node(self.entityIndex, "id", str(entityId))
        if node is not None:
            rels = node.get_relationships()
            for rel in rels:
                self.graphDB.delete(rel)
            self.graphDB.delete(node)
            return True
        return False

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

    def GetScalarResults(self, neoResult):
        items = []
        for result in neoResult[0]:
            item = result[0]
            items.append(item)
        return items

    def GetScalarResult(self, neoResult):
        items = self.GetScalarResults(neoResult)
        if len(items) > 0:
            return items[0]
        return None

    def GetNextId(self):
        query = "start n = node:{0}('id:*') return Max(n.id)".format(self.entityIndex)
        result = self.executeQuery(query)
        maxId = self.GetScalarResult(result)
        if isinstance(maxId, int):
            return maxId + 1
        return -1

    def executeQuery(self, query):
        neoResult = cypher.execute(self.GetGraphDb(), query)
        return neoResult




__author__ = 'funhead'
