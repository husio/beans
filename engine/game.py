import collections
import itertools
import random

from engine import card
from engine.errors import GameError, GameEnd


START_CARD_NUMBER = 5


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
        self.active_player = None
        self.players = collections.OrderedDict()
        self._users_iter = None

    def start(self):
        if len(self.players) < 2:
            raise GameError("not enough players")
        self._users_iter = itertools.cycle(self.players.values())
        for player in self.players.values():
            for _ in range(START_CARD_NUMBER):
                player.hand.append(self.deck.draw_card())
        self.active_player = next(self._users_iter)

    def next_turn(self):
        self.active_player = next(self._users_iter)

    def add_player(self, player):
        if player._game:
            raise GameError("player already in game")
        self.players[player.pid] = player
        player._game = self

    def remove_player(self, player_or_pid):
        pid = getattr(player_or_pid, 'pid', player_or_pid)
        player = self.players.pop(pid, None)
        if not player:
            raise GameError("player not in this game")
        player.game = None
