from src.players.player import Player
from src.enums.player_type import PlayerType


class Human(Player):
  """
  @todo implement a human player that can play against a trained agent
  """

  def __init__(self):
    super(Human, self).__init__(PlayerType.HUMAN)
    pass
