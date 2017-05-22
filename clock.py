# Clock
class Clock:
    def __init__(self):
        self._current_time = 0

    def increment(self):
        self._current_time += 1

    def get_current_time(self):
        return self._current_time

    def reset_time(self):
        self._current_time = 0
