from src.state.state import State
from src.enums.marker import Marker


def get_all_states_impl(current_state: State, marker: Marker, all_states: dict) -> None:
  """
  Get all states following the current state, recursively.

  :param current_state: The current state
  :type current_state: State
  :param marker: The current marker to position on the tic-tac-toe board
  :type marker: Marker
  :param all_states: A list of all states, previous as well as future
  :type all_states: dict

  :rtype: None
  """
  for i in range(State.DIMENSIONS):
    for j in range(State.DIMENSIONS):
      # if there are no markers on the position (i, j) for the current state, get the next possible states.
      if current_state.state[i][j] == 0:
        new_state = current_state.next_state(marker, (i, j))

        if new_state.hash not in all_states:
          all_states[new_state.hash] = (new_state, new_state.is_end_state)

          if not new_state.is_end_state:
            # get next states based on what the opponent will play
            if marker == Marker.CROSS:
              other_marker = Marker.NOUGHTS
            else:
              other_marker = Marker.CROSS

            get_all_states_impl(new_state, other_marker, all_states)


def get_all_states() -> dict:
  """
  Get all states following the current symbol

  :rtype: dict
  """
  current_symbol = Marker.CROSS
  current_state = State()

  all_states = dict()
  all_states[current_state.hash] = (current_state, current_state.is_end_state)
  get_all_states_impl(current_state, current_symbol, all_states)

  return all_states
