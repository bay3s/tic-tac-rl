from abc import ABC
from src.enums.player_type import PlayerType


class Player(ABC):

  def __init__(self, type: PlayerType):
    """
    Initialize the player.

    :param type: The type of player to initialize (either human or computer).
    :type type: PlayerType
    """
    self._type = type

  @property
  def type(self) -> PlayerType:
    """
    The type of player that has been initialized (either human or computer).

    :rtype: PlayerType
    """
    return self._type
