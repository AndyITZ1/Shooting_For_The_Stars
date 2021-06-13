from game import Game

# Icon made by Freepik from www.flaticon.com

game = Game()

while True:
    game.menu.display_menu()
    game.game_loop()
