from engine import counter


class Bohne:
    __gen_cid = counter.NumberGenerator()

    num_in_deck = NotImplemented
    exchange_rate = NotImplemented
    name = NotImplemented

    def __init__(self):
        self.cid = self.__gen_cid()

    def __repr__(self):
        return "{}#{}".format(type(self).__name__, self.cid)


class Saubohne(Bohne):
    name = "Saubohne"
    num_in_deck = 16
    exchange_rate = (None, 0, 0, 1, 1, 2, 2, 3, 4)


class Sojabohne(Bohne):
    name = "Sojabohne"
    num_in_deck = 12
    exchange_rate = (None, 0, 1, 1, 2, 2, 3, 4)


class Kakaobohne(Bohne):
    name = "kakaobohne"
    num_in_deck = 4
    exchange_rate = (None, 0, 2, 3, 4)
