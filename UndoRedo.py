import copy

class Caretaker:
    def __init__(self, game_state):
        self._game_state_mementos = [copy.deepcopy(game_state)]
        self._current_index = 0

    def save(self, game_state):
        # If we're in the middle of the memento list due to undos and we make a new move,
        # we need to remove the 'future' states before saving the new state.
        if self._current_index < len(self._game_state_mementos) - 1:
            self._game_state_mementos = self._game_state_mementos[:self._current_index + 1]
        self._game_state_mementos.append(copy.deepcopy(game_state))
        self._current_index += 1

    def undo(self):
        if self._current_index > 0:
            self._current_index -= 1
            return self._game_state_mementos[self._current_index]
        return None

    def redo(self):
        if self._current_index < len(self._game_state_mementos) - 1:
            self._current_index += 1
            return self._game_state_mementos[self._current_index]
        return None