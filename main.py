#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import time
import bdd
import random
import tornado.ioloop
import tornado.web
import json

#from Modules.UnixSysInfos import *
#from __builtin__ import file

__title__ = "Nuit de l'info 2015 - Binouse"

# var : directory name where the server will load in "pages" and "rsc"
filePath = "static/"


# Handler for api
class APIHandler(tornado.web.RequestHandler):
    def get(self, path_request):
        #self.write("API [" + str(time.time()) + "]: GET " + path_request)
        if path_request == "random":
            self.write(str(random.randint(0, 100)))
        elif path_request == "timestamp":
            self.write(str(time.time()))
        elif path_request == "test":
            jsonVar = {"records": []}
            catas = bdd.getCata()
            for cata in catas:
                jsonVar["records"].append({"id": cata[0], "Name": cata[1], "Status": "", "DerniereActu": {"Date": "01234567890", "Description": "blablabla"}})
            self.write(json.dumps(jsonVar))
        else:
            self.set_status(400)
            self.write("Bad Request")

    def post(self, path_request):
        self.set_status(501)
        self.write("Not Implemented")

    def put(self, path_request):
        self.set_status(501)
        self.write("Not Implemented")

    def delete(self, path_request):
        self.set_status(501)
        self.write("Not Implemented")



# Handler for index page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(open(filePath + "index.html", 'rb').read())


def main():

    if os.path.isfile("example.db"):
        bdd.suprTables()
    bdd.creaTables()
    bdd.creaTuples()

    application = tornado.web.Application(
        [
            (r"/API/(.*)$", APIHandler),
            (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': filePath+'img/'}),
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': filePath+'css/'}),
            (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': filePath+'js/'}),
            (r"/", MainHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {'path': filePath}),
        ],
        autoreload=True,
        debug=True
    )   # create an instance

    if os.path.isfile("cert/default.key") and os.path.isfile("cert/default.cert"):
        # bind https port
        application.listen(4430, ssl_options={"certfile": os.path.join("cert/default.cert"),
                                              "keyfile": os.path.join("cert/default.key"),
                                              "cert_reqs": ssl.CERT_OPTIONAL})
    # bind http port
    application.listen(8080)
    # loop forever for satisfy user's requests
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
