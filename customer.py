class Customer:
    #Customers wait in line, and know how long they waited in line
    def __init__(self):
        self._time_spent_in_line = 0

    def increment_wait_time(self):
        self._time_spent_in_line += 1

    def get_time_spent_in_line(self):
        return self._time_spent_in_line

