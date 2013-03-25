__author__ = 'MichaelI'

import unittest
from data.NeoData.SourceRepository import SourceRepository
from service import Resource
import simplejson


class ServiceTest(unittest.TestCase):
    def testSourcePut(self):
        sourceService = Resource(SourceRepository())
        source = sourceService.set_item('{"id":3,"title":"The Telegraph","readership":404222}')
        self.assertIsNotNone(sourceService)


#{"id":3,"title":"The Telegraph","readership":404222}

if __name__ == '__main__':
    unittest.main()
