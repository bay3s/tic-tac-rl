from src.players.computer import Computer
from src.state.state import State
from src.state.helper import get_all_states
from typing import Generator


class Game:

    def __init__(self, player_one: Computer, player_two: Computer) -> None:
      """
      Initialize the game with two players and a starting state.

      :param player_one: The first player that is part of this game.
      :type player_one: Computer
      :param player_two: The second player that is part of this game.
      :type player_two: Computer

      :rtype None
      """
      self.current_state = State()
      self.player_one = player_one
      self.player_two = player_two
      self.total_moves_made = 0.

    def reset(self) -> None:
      """
      Resets state history for both players.

      :return: None
      :rtype: None
      """
      self.player_one.reset()
      self.player_two.reset()
      self.total_moves_made = 0.

    def alternate(self) -> Generator[Computer, None, None]:
      """
      Alternates between returning either player one or player two depending on whose turn it is to play the game.

      :return: None
      :rtype: None
      """
      while True:
        yield self.player_one
        yield self.player_two

    def play(self, debug=False) -> Computer:
      """
      Play the game given the two players that it is instantiated until we find a winner or we get to an end state.

      :rtype None
      """
      alternator = self.alternate()
      possible_states = get_all_states()
      self.reset()

      current_state = State()
      self.player_one.extend_state_history(current_state)
      self.player_two.extend_state_history(current_state)

      if debug:
        print(current_state)

      while True:
        player = next(alternator)
        i, j = player.next_action()
        self.total_moves_made += 1

        next_state_hash = current_state.next_state(player.marker, (i, j)).hash
        next_state, is_end = possible_states[next_state_hash]

        self.player_one.extend_state_history(next_state)
        self.player_two.extend_state_history(next_state)

        # update the current state to reflect the state transition
        current_state = next_state

        if debug:
          print(current_state)

        if is_end:
          if current_state.winning_marker == self.player_one.marker:
            return self.player_one
          else:
            return self.player_two
