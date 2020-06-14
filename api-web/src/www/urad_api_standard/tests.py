import json
from urad_api.base import BaseUnitTest

class StandardUnitTest(BaseUnitTest):
    def set_headers(self, headers = {}):
        self.headers = headers
    def get(self, message = '', url = ''):
        print "\n"
        print "********************************************"
        print "[x] " + message
        print "GET: " + url
        response = self.client.get(url, **self.headers)
        print "RESPONSE: "
        print response
        print "\n"
        print "DATA:"
        print json.dumps(json.loads(response.content), indent=4)
        print "\n"
    def post(self, message = '', url = '', data = {}):
        print "\n"
        print "********************************************"
        print "[x] " + message
        print "GET: " + url
        response = self.client.post(url, json.dumps(data), content_type="application/json", **self.headers)
        print "RESPONSE: "
        print response
        print "\n"
        print "DATA:"
        print json.dumps(json.loads(response.content), indent=4)
        print "\n"
