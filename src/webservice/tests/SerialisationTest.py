__author__ = 'MichaelI'

import unittest
import simplejson
from entities.CoreEntities import Document


class SerialisationTest(unittest.TestCase):
    def test_something(self):
        doc = simplejson.loads(self.GetDocumentJson())
        document = Document()
        document.__dict__.update(doc)
        self.assertIsNotNone(document)

    def GetDocumentJson(self):
        json = '{ \
                    "id": 201, \
                    "title": "Cyprus bailout deal with EU closes bank and seizes large deposits", \
                    "date": 20120325, \
                    "sourceid": 1, \
                    "author": { \
                                  "firstName": "Dave", \
                                  "lastName": "Jones" \
                              }, \
                    "flags": [ \
                        { \
                            "id": 23, \
                            "title": "Message 1", \
                            "category": { \
                                "id": 10, \
                                "title": "Messages", \
                                "type": 1 \
                            } \
                        }, \
                        { \
                            "id": 62, \
                            "title": "Spokesperson 1", \
                            "category": { \
                                "id": 11, \
                                "title": "Spokespeople", \
                                "type": 3 \
                            } \
                        }, \
                        { \
                            "id": 345, \
                            "title": "Headline Mention", \
                            "category": { \
                                "id": 4, \
                                "title": "Prominence", \
                                "type": 1 \
                            } \
                        } \
                    ] \
                }'
        return json

if __name__ == '__main__':
    unittest.main()
