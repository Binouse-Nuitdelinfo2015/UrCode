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
        elif path_request == "test":
            jsonVar = {"records": []}
            catas = bdd.getCata()
            for cata in catas:
                jsonVar["records"].append({"id": cata[0], "Name": cata[1], "Status": "", "DerniereActu": {"Date": "01234567890", "Description": "blablabla"}})
            self.write(json.dumps(jsonVar))


# Handler for ressources
class RscHandler(tornado.web.RequestHandler):
    def get(self, path_request):
        if str(path_request).endswith(".css"):
            self.set_header("Content-Type", "text/css; charset=UTF-8")
        self.write(open(filePath + "css/" + path_request, 'rb').read())


# Handler for HTML files
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(open(filePath + "index.html", 'rb').read())

    def post(self):
        try:
            action = self.get_argument("action")
            print("action :", action)
        except tornado.web.HTTPError:   # no or wrong arguments
            pass
        self.write(open(filePath + "index.html", 'rb').read())


def main():

    bdd.suprTables()
    bdd.creaTables()
    bdd.creaTuples()

    application = tornado.web.Application(
        [
            (r'/static/img/(.*)', tornado.web.StaticFileHandler, {'path': 'static/img/'}),
            (r'/static/css/(.*)', tornado.web.StaticFileHandler, {'path': 'static/css/'}),
            (r'/static/js/(.*)', tornado.web.StaticFileHandler, {'path': 'static/js/'}),
            (r"/API/(.*)$", APIHandler),
            (r"/", MainHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {'path': 'static/'}),
        ],
        autoreload=True,
        debug=True
    )   # create an instance

    if(os.path.isfile("cert/" + "default.key") and
       os.path.isfile("cert/" + "default.cert")):
        # bind https port
        application.listen(4430, ssl_options={"certfile": os.path.join("cert/" + "default.cert"), "keyfile": os.path.join("cert/" + "default.key"), "cert_reqs": ssl.CERT_OPTIONAL})

    # bind http port
    application.listen(8080)
    # loop forever for satisfy user's requests
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
