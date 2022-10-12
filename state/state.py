import numpy as np
from src.players.player import Player
from src.enums.marker import Marker
from copy import deepcopy


class State:

  DIMENSIONS = 3

  def __init__(self):
    """
    Constructor for the tic-tac-toe state.

    :rtype None
    """
    self._state = np.zeros((State.DIMENSIONS, State.DIMENSIONS))

    self._winning_marker = None
    self._is_end_state = None
    self._evaluated = False
    pass

  @property
  def state(self) -> np.array:
    """
    Returns the current state of the state

    :rtype: np.array
    """
    return self._state

  @property
  def hash(self) -> str:
    """
    Returns a unique has based on the current state state.

    :rtype: str
    """
    return hash(self.state.tostring())

  @property
  def winning_marker(self) -> Player:
    return self._winning_marker

  @property
  def is_end_state(self) -> bool:
    return self._is_end_state

  def next_state(self, marker: Marker, position: (int, int)) -> np.array:
    """
    Gets the next state given a the current state and the input position of the marker.

    :param marker: Marker to move into the position.
    :type marker: Marker
    :param position: The position on which the player is making the move.
    :type position: tuple

    :rtype: np.array
    """
    temp = deepcopy(self._state)

    if temp[position[0], position[1]] != 0.:
      raise Exception(f'Invalid position supplied for state update, marker already present in current position.')

    temp[position[0], position[1]] = marker.value

    new_state = State()
    new_state._state = temp
    new_state.evaluate()

    return new_state

  def evaluate(self) -> [bool, Marker]:
    """
    Returns True if the state is over along with the winning player (if any), False otherwise.

    :rtype: [bool, Player]
    """
    if self._evaluated is True:
      return self._is_end_state, self._winning_marker

    results = list()

    for i in range(State.DIMENSIONS):
      results.append(np.sum(self.state[i, :]))
      results.append(np.sum(self.state[:, i]))

    trace = 0
    reverse_trace = 0

    for i in range(State.DIMENSIONS):
      trace += self.state[i, i]
      reverse_trace += self.state[i, State.DIMENSIONS - 1 - i]

    results.append(trace)
    results.append(reverse_trace)

    for result in results:

      if result == 3 * Marker.CROSS.value:
        self._winning_marker = Marker.CROSS
        self._is_end_state = True
        self._evaluated = True

        return self._is_end_state, self._winning_marker

      if result == 3 * Marker.NOUGHTS.value:
        self._winning_marker = Marker.NOUGHTS
        self._is_end_state = True
        self._evaluated = True

        return self._is_end_state, self._winning_marker

    num_total_moves = np.sum(np.abs(self.state))

    # check if all moves have been played - if there is no winner at this point, it's a tie
    if num_total_moves == State.DIMENSIONS ** 2:
      self._winning_marker = None
      self._is_end_state = True
      self._evaluated = True

      return self._is_end_state, self._winning_marker

    self._is_end_state = False
    self._evaluated = True

    return self._is_end_state, None

  def __str__(self) -> str:
    """
    Returns the current state of the board as a string

    :rtype: str
    """
    out = '------------- \n'

    for i in range(State.DIMENSIONS):
      out += '| '

      for j in range(State.DIMENSIONS):
        if self._state[i, j] == 1:
          token = 'x'
        elif self._state[i, j] == -1:
          token = 'o'
        else:
          token = ' '

        out += token + ' | '

      out += '\n'

    out += '------------- \n'

    return out
