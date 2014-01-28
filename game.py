import collections
import itertools
import random

import card
import counter


class GameEnd(Exception):
    pass


class Field:
    def __init__(self):
        self._rows = [[], []]

    def plant(self, row_no, bohne):
        row = self._rows[row_no]
        if row and type(row[0]) != type(bohne):
            raise TypeError("bohne type missmatch")
        row.append(bohne)

    def harvest(self, row_no):
        row = self._rows[row_no]
        if not row:
            return ((), ())
        coins_count = type(row[0]).exchange_rate(len(row))
        coins = row[:coins_count]
        grave = row[coins_count:]
        row.clear()
        return (coins, grave)

    def extend(self):
        if len(self._rows) == 3:
            raise Exception("cannot extend")
        self._rows.append([])

    def rows(self):
        return self._rows


class Player:
    __gen_pid = counter.NumberGenerator()

    def __init__(self, name):
        self.name = name
        self.pid = self.__gen_pid()
        self.game = None
        self.coins = []
        self.hand = collections.deque()
        self.field = Field()

    def draw_card(self):
        return self.game.draw_card()

    def plant(self, row_no, bohne):
        self.field.plant(row_no, bohne)

    def harvest(self, row_no):
        coins, grave = self.field.harvest(row_no)
        self.coins.extend(coins)
        self.game.graveyard.extend(grave)


class Deck:
    def __init__(self, *card_types):
        self.shuffle_count = 0
        self.game_pile = collections.deque()
        self.graveyard = collections.deque()

        for card_type in card_types:
            for _ in range(card_type.num_in_deck):
                self.game_pile.append(card_type())
        random.shuffle(self.game_pile)

    def draw_card(self):
        try:
            return self.game_pile.pop()
        except IndexError:
            if self.shuffle_count > 2:
                raise GameEnd
        self.shuffle_count += 1
        cards = self.graveyard
        self.graveyard = []
        random.shuffle(cards)
        self.game_pile.extend(cards)
        return self.draw_card()


class Game:
    def __init__(self):
        self.deck = Deck(card.Saubohne, card.Sojabohne, card.Kakaobohne)
        self.turn = 0
        self.active_player = None
        self._players = collections.OrderedDict()
        self._users_iter = None
        self._trade_beans = ()

    def start(self):
        if len(self._players) < 2:
            raise Exception("not enough players")
        self._users_iter = itertools.cycle(self._players.values())
        for player in self._players.values():
            for _ in range(5):
                player.hand.append(self.deck.draw_card())
        self.active_player = next(self._users_iter)

    def draw_trade_beans(self):
        self._trade_beans = (self.deck.draw_card(), self.deck.draw_card())
        return self._trade_beans

    def next_turn(self):
        self.turn += 1
        self.active_player = next(self._users_iter)
        if self._trade_beans:
            raise Exception("not all beans were traded")

    def join_player(self, player):
        if player.game:
            raise Exception("player already in game")
        self._players[player.pid] = player
        player.game = self

    def remove_player(self, player_or_pid):
        pid = getattr(player_or_pid, 'pid', player_or_pid)
        player = self.players.pop(pid, None)
        if not player:
            raise Exception("player not in this game")
        player.game = None
