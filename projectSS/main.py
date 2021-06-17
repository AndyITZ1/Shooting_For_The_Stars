from projectSS.game import Game

# Icon made by Freepik from www.flaticon.com


def main():
    game = Game()
    while True:
        game.menu.display_menu()
        game.game_loop()


if __name__ == "__main__":
    main()
