import collections
import unittest


from engine.card import Saubohne, Sojabohne
from engine.game import Game
from engine.player import Player

beans = (
    Saubohne(), Saubohne(), Saubohne(), Saubohne(), Saubohne(),
    Saubohne(), Sojabohne(), Sojabohne(), Sojabohne(), Sojabohne(),
    Saubohne(), Saubohne(), Saubohne(), Sojabohne(), Saubohne(),
    Sojabohne(), Sojabohne(), Sojabohne(), Sojabohne(), Sojabohne(),
)[::-1]


def bean_cids(beans):
    return [bean.cid for bean in beans]


class SimpleGameTest(unittest.TestCase):
    def test_simple_game(self):
        game = Game()
        game.deck.game_pile = collections.deque(beans)

        player_1 = Player("bob")
        game.add_player(player_1)
        player_2 = Player("mike")
        game.add_player(player_2)

        game.start()

        # 5 saubohne
        self.assertEqual(bean_cids(player_1.hand), [1, 2, 3, 4, 5])
        self.assertEqual(player_1.field.rows, [[], []])
        # 1 saubohne, 4 sojabohne
        self.assertEqual(bean_cids(player_2.hand), [6, 7, 8, 9, 10])
        self.assertEqual(player_2.field.rows, [[], []])

        self.assertEqual(game.active_player, player_1)

        player_1.plant_from_hand(0)
        player_1.plant_from_hand(0)
        self.assertEqual(bean_cids(player_1.field.rows[0]), [1, 2])
        # trade cards - saubohne #11 & #12
        player_1.plant(0, player_1.draw_card())
        player_1.plant(0, player_1.draw_card())
        self.assertEqual(bean_cids(player_1.field.rows[0]), [1, 2, 11, 12])
        self.assertEqual(bean_cids(player_1.hand), [3, 4, 5])
        player_1.end_turn()
        self.assertEqual(bean_cids(player_1.hand), [3, 4, 5, 13, 14, 15])

        self.assertEqual(game.active_player, player_2)
        player_2.plant_from_hand(1)
        self.assertRaises(TypeError, player_2.plant_from_hand, 1)

        trade_cards = (player_2.draw_card(), player_2.draw_card())
        # 2x Sojabohne
        self.assertEqual(bean_cids(trade_cards), [16, 17])
        self.assertRaises(TypeError, player_2.plant, 1, trade_cards[0])
        player_2.plant(0, trade_cards[0])
        player_2.plant(0, trade_cards[1])
        player_2.end_turn()

        game.remove_player(player_1)
        game.remove_player(player_2)




if __name__ == "__main__":
    unittest.main()
