#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import time
import random
import tornado.ioloop
import tornado.web
import json

#from Modules.UnixSysInfos import *
#from __builtin__ import file

__title__ = "Nuit de l'info 2015 - Binouse"

# var : directory name where the server will load in "pages" and "rsc"
filePath = "static/"

#def liste_dump(folder):
#    dico = {}
#    for root, dirs, files in os.walk(folder):
#        for dump in files:
#            path = "./" + root + "/" + dump
#            dico[dump] = open(path).read().replace("login:", "").replace("password:", "").split("\n")[:-1]
#    return dico


# Handler for api
class APIHandler(tornado.web.RequestHandler):
    def get(self, path_request):
        #self.write("API [" + str(time.time()) + "]: GET " + path_request)
        if path_request == "random":
            self.write(str(random.randint(0, 100)))
        elif path_request == "test":
            self.write(
                json.dumps(
                    {
                        "records":
                            [
                                {
                                    "id": "0",
                                    "Name": "test",
                                    "Status": "test",
                                    "DerniereActu":
                                        {
                                            "Date": "123456789",
                                            "Description": "blablabla"
                                        }
                                },
                                {
                                    "id": "0",
                                    "Name": "test",
                                    "Status": "test",
                                    "DerniereActu":
                                        {
                                            "Date": "123456789",
                                            "Description": "blablabla"
                                        }
                                }
                            ]
                    }
                )
            )


# Handler for ressources
class RscHandler(tornado.web.RequestHandler):
    def get(self, path_request):
        if str(path_request).endswith(".css"):
            self.set_header("Content-Type", "text/css; charset=UTF-8")
        self.write(open(filePath + "css/" + path_request, 'rb').read())


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/admin/index.html")

    def post(self):
        try:
            action = self.get_argument("action")
            print("action :", action)
        except tornado.web.HTTPError:   # no or wrong arguments
            pass
        self.render("pages/admin/index.html")


# Handler for HTML files
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(open(filePath + "index.html", 'rb').read())


def main():
    application = tornado.web.Application(
        [
            (r'/static/img/(.*)', tornado.web.StaticFileHandler, {'path': 'static/img/'}),
            (r'/static/css/(.*)', tornado.web.StaticFileHandler, {'path': 'static/css/'}),
            (r'/static/js/(.*)', tornado.web.StaticFileHandler, {'path': 'static/js/'}),
            (r"/admin", AdminHandler),
            (r"/admin/.*", AdminHandler),
            (r"/API/(.*)$", APIHandler),
            (r"/", MainHandler),
            (r"/.*", MainHandler),
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
