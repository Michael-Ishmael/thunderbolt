from py2neo import rest, neo4j

uri = "http://localhost:7474/db/data/"
publicationRefId = 0


def TestGraph():
    try:
        graph_db = neo4j.GraphDatabaseService(uri)
        print graph_db.neo4j_version
    except rest.NoResponse:
        print "Cannot connect to host"
    except rest.ResourceNotFound:
        print "Database service not found"


def CreatePublicationNodes():
    graph_db = neo4j.GraphDatabaseService(uri)
    publicationRefNode = graph_db.get_node(6)
    publicationRefId = publicationRefNode.id
    references = graph_db.get_or_create_index(neo4j.Node, "references")
    references.add("reference", "source", publicationRefNode)
    references.add("id", 1, publicationRefNode)
    sources = graph_db.get_or_create_index(neo4j.Node, "sources")
    pub1, pub2, pub3 = graph_db.create({"id": 1, "title": "The Guardian", "readership": 204222, "pagerate": 3000},
                                       {"id": 2, "title": "The Times", "readership": 304222, "pagerate": 4000},
                                       {"id": 3, "title": "The Telegraph", "readership": 404222, "pagerate": 2500})
    sources.add("id", 1, pub1)
    sources.add("id", 2, pub2)
    sources.add("id", 3, pub3)

    publicationRefNode.create_relationship_to(pub1, "SOURCE")
    publicationRefNode.create_relationship_to(pub2, "SOURCE")
    publicationRefNode.create_relationship_to(pub3, "SOURCE")

    print(publicationRefId)


__author__ = 'MichaelI'
