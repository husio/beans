import collections

from engine import counter
from engine.errors import GameError


class Field:
    def __init__(self):
        self.rows = [[], []]

    def plant(self, row_no, bean):
        row = self.rows[row_no]
        if row and type(row[0]) != type(bean):
            msg = "bean type missmatch {} != {}".format(bean.name, row[0].name)
            raise GameError(msg)
        row.append(bean)

    def harvest(self, row_no):
        "Return (coins, grave) pair of cards"
        row = self.rows[row_no]
        if not row:
            return ((), ())
        coins_count = type(row[0]).exchange_rate(len(row))
        coins = row[:coins_count]
        grave = row[coins_count:]
        row.clear()
        return (coins, grave)

    def extend(self):
        if len(self.rows) == 3:
            raise GameError("cannot extend")
        self.rows.append([])


class Player:
    __gen_pid = counter.NumberGenerator()

    def __init__(self, name=None):
        self.pid = self.__gen_pid()
        self.name = name or "Anonymous{}".format(self.pid)
        self._game = None
        self.coins = []
        self.hand = collections.deque()
        self.field = Field()

    def draw_card(self):
        return self._game.deck.draw_card()

    def plant(self, row_no, bean):
        self.field.plant(row_no, bean)

    def plant_from_hand(self, row_no):
        bean = self.hand[0]
        self.plant(row_no, bean)
        # do not remove from hand until we're sure the bean can be planted
        self.hand.popleft()

    def harvest(self, row_no):
        coins, grave = self.field.harvest(row_no)
        self.coins.extend(coins)
        self._game.graveyard.extend(grave)

    def end_turn(self):
        self.hand.append(self.draw_card())
        self.hand.append(self.draw_card())
        self.hand.append(self.draw_card())
        self._game.next_turn()
