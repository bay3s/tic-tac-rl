import numpy as np
from src.state.state import State
from src.enums.marker import Marker
from src.enums.player_type import PlayerType
from src.state.helper import get_all_states as get_all_states
from src.players.player import Player


class Computer(Player):

  def __init__(self, marker: Marker, learning_rate: float, epsilon: float) -> None:
    """
    Initialize a player.

    :param marker: Marker to assign to the player.
    :type marker: Marker
    :param learning_rate: Step-size for the temporal-difference learning.
    :type learning_rate: float
    :param epsilon: Epsilon value for epsilon-greedy.
    :type epsilon: float

    :rtype None
    """
    super(Computer, self).__init__(PlayerType.COMPUTER)

    self.marker = marker
    self.learning_rate = learning_rate
    self.epsilon = epsilon

    # tracks the history of states for the player.
    self.state_history = list()

    # tracks the value estimates for being in specific states - each state has a unique hash value.
    self.estimated_state_values = dict()

    # initialize state value estimates for the player.
    self.init_value_estimates()

  def get_opponent_marker(self) -> Marker:
    """
    Give the marker for the player, return the marker for the opponent.

    :rtype: Marker
    """
    if self.marker == Marker.CROSS:
      return Marker.NOUGHTS

    return Marker.CROSS

  def reset(self) -> None:
    """
    Resets the state history for the player.

    :rtype: None
    """
    self.state_history = []

  def extend_state_history(self, state: np.array) -> None:
    """
    Extend the history of states for the current player.

    :param state: The state of the state.
    :type state: np.array

    :rtype: None
    """
    self.state_history.append({
      'state': state,
      # the type of move to be made from this state is yet to be determined
      'is_greedy_move': None
    })

  def init_value_estimates(self) -> None:
    """
    Generate value estimates for each state of the tic-tac-toe board.

    :rtype: None
    """
    all_states = get_all_states()

    for hash_val in all_states:
      state, is_end = all_states[hash_val]

      if is_end:
        if state.winning_marker == self.marker:
          # win
          self.estimated_state_values[hash_val] = 1.0
        elif state.winning_marker is None:
          # tie
          self.estimated_state_values[hash_val] = 0.5
        else:
          # lose
          self.estimated_state_values[hash_val] = 0
      else:
        self.estimated_state_values[hash_val] = 0.5

  def backup(self):
    """
    Update value estimates based on the TD error.

    :rtype: None
    """
    for i in reversed(range(len(self.state_history) - 1)):
      # compute the TD error for each greedy move, starting with the last one all the way down to the first.
      is_greedy = self.state_history[i]['is_greedy_move']
      td_error = (self.estimated_state_values[self.state_history[i + 1]['state'].hash] -
                  self.estimated_state_values[self.state_history[i]['state'].hash]) * is_greedy

      # backup the TD error at each step.
      self.estimated_state_values[self.state_history[i]['state'].hash] += self.learning_rate * td_error

  def next_action(self) -> [int, int]:
    """
    This is basically the policy that we follow during the state play, exploration done using epsilon-greedy
    based on the epsilon value provided for the constructor.

    :rtype: [int, int]
    """
    state = self.state_history[-1]['state']
    next_states = []
    next_positions = []

    for i in range(State.DIMENSIONS):
      for j in range(State.DIMENSIONS):
        if state.state[i, j] == 0:
          next_positions.append([i, j])
          next_states.append(state.next_state(self.marker, (i, j)).hash)

    # explore
    if np.random.rand() < self.epsilon:
      action = next_positions[np.random.randint(len(next_positions))]
      self.state_history[-1]['is_greedy_move'] = False

      return action

    values = []
    for hash_val, pos in zip(next_states, next_positions):
        values.append((self.estimated_state_values[hash_val], pos))

    # exploit, shuffling assures that we choose different actions each time given multiple actions with the same value.
    np.random.shuffle(values)
    values.sort(key=lambda x: x[0], reverse=True)
    action = values[0][1]
    self.state_history[-1]['is_greedy_move'] = True

    return action
