import os

import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.websocket
from sockjs.tornado import SockJSRouter, SockJSConnection

from engine.rules import Gameplay, InvalidCall


DEBUG = True
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FILES_PATH = os.path.join(PROJECT_DIR, 'static')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")


game = Gameplay()


class GameClientConnection(SockJSConnection):
    clients = set()

    def on_open(self, info):
        self.player = game.add_player()
        self.broadcast(self.clients, {"message": "someone joined"})
        self.clients.add(self)

    def on_message(self, message):
        try:
            response = game.handle_action(self.player, message)
            self.broadcast(self.clients, response)
        except InvalidCall as exc:
            response = {
                "error": "invalid call",
                "text": str(exc),
                "message": message,
            }
            self.broadcast(self.clients, response)
        except Exception as exc:
            response = {
                "error": "error",
                "text": str(exc),
                "message": message,
            }
            self.send(response)

    def on_close(self):
        self.clients.remove(self)
        self.broadcast(self.clients, {"message": "someone left"})


routing = [
    (r"/", IndexHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': STATIC_FILES_PATH}),
] + SockJSRouter(GameClientConnection, "/socket").urls

application = tornado.web.Application(routing, debug=DEBUG)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
