from src.players.computer import Computer
from src.game.game import Game
from src.enums.marker import Marker


epochs = 10_000

player_one_wins_total = 0.0
player_two_wins_total = 0.0

player_one_last_10 = 0.0
player_two_last_10 = 0.0


player_one = Computer(marker=Marker.CROSS, learning_rate = 0.1, epsilon=0.01)
player_two = Computer(marker=Marker.NOUGHTS, learning_rate = 0.1, epsilon=0.01)

game = Game(player_one, player_two)

for i in range(1, epochs + 1):
  winning_player = game.play(debug=False)

  if winning_player is player_one:
    player_one_wins_total += 1
    player_one_last_10 += 1

  if winning_player is player_two:
    player_two_wins_total += 1
    player_two_last_10 += 1

  if i % 100 == 0:
    win_rate_player_one = round(player_one_last_10 / 100, 2)
    win_rate_player_two = round(player_two_last_10 / 100, 2)

    print(f'Player 1 (Win Rate): {win_rate_player_one}, Player 2 (Win Rate): {win_rate_player_two}')
    player_one_last_10 = 0
    player_two_last_10 = 0
    pass

  player_one.backup()
  player_two.backup()

  game.reset()
