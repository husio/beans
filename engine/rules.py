import weakref

import engine.game
import engine.player


class InvalidCall(Exception):
    pass


class Turn:
    def __init__(self, game):
        self.game = weakref.proxy(game)
        self.trade_draw = None

    def play_bean(self):
        raise NotImplemented

    def trade(self, beans, player):
        pass


class Handler:
    def __init__(self, game):
        self.game = game

    def set_player_name(self, player, name):
        player.name = name



class Gameplay:
    def __init__(self, ):
        self.handler = Handler(engine.game.Game())

    def handle_action(self, player, command, *args):
        if command.startswith('_'):
            raise InvalidCall("unknown command \"{}\"".format(command))
        func = getattr(self.handler, command, None)
        if func is None:
            raise InvalidCall("unknown command \"{}\"".format(command))
        return func(player, *args)

    def remove_player(self, player):
        self.handler.game.remove_player(player)

    def add_player(self, name=None):
        player = engine.player.Player(name)
        self.handler.game.add_player(player)
        return player
