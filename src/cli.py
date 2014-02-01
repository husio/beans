import os

from game import Player, Game, GameEnd


def clear_screen():
    os.system("clear")


def print_state(player):
    clear_screen()
    print("turn {}".format(player.game.turn))
    for i, row in enumerate(player.field.rows()):
        if row:
            info = " {} {} planted".format(len(row), row[0].name)
        else:
            info = " nothing planted"
        print("{} row: {}".format(i, info))
    print("hand: {}".format(", ".join(bean.name for bean in player.hand)))


def play_turn(player):
    print_state(player)
    if player.hand:
        to_play = input("play beans [y/N]: ")
        if to_play in 'yY':
            player.plant(0, player.hand.popleft())
    trade_beans = player.game.draw_trade_beans()
    print("trade beans: {}".format(
        ", ".join(bean.name for bean in trade_beans)))
    input("what to do?!")


def run_cli():
    player_1 = Player("Player 1")
    player_2 = Player("Player 2")
    game = Game()
    game.join_player(player_1)
    game.join_player(player_2)
    game.start()
    try:
        while True:
            play_turn(game.active_player)
    except GameEnd:
        print("game end")
        import pdb; pdb.set_trace()


if __name__ == "__main__":
    run_cli()
