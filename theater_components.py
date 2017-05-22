from queue33 import Queue
from clock import Clock
from customer import Customer
from simulation_events import *
from statistics import *

import random

# Theater, ticket window, ticket line
class TicketLine:
    def __init__(self, line_num: int, clock: Clock):
        self._line_num = line_num
        self._clock = clock
        self._queue = Queue()

        # Statistics
        self._max_length = 0
        self._customer_wait_times = []

    def __str__(self):
        result = 'Line #{}'.format(self._line_num) + ": "
        result += str(list(self._queue))
        return result

    def __len__(self):
        return len(self._queue)

    def get_statistics(self):
        return TicketLineStatistics(len(self), self._max_length, self._customer_wait_times)

    def is_empty(self):
        return len(self._queue) == 0

    def get_line_num(self):
        return self._line_num

    def enqueue_customer(self, customer: Customer):
        self._queue.enqueue(customer)

        if len(self._queue) > self._max_length:
            self._max_length = len(self._queue)

    def dequeue_customer(self):
        first_in_line = self._queue.front()
        self._customer_wait_times.append(first_in_line.get_time_spent_in_line())
        return self._queue.dequeue()

    def update_waiting_times(self):
        for customer in self._queue:
            customer.increment_wait_time()


class TicketWindow:
    def __init__(self, window_num: int, processing_time: int, clock: Clock):
        self._window_num = window_num
        self._processing_time = processing_time
        self._clock = clock

        # Current customer processing
        self._current_customer = None
        self._begin_processing_time = 0

        # Statistics
        self._tickets_sold = 0
        self._idle_time = 0


    def __str__(self):
        return "Window #{} ({} secs): Current Customer = {}".\
            format(self._window_num, self._processing_time, self._current_customer)

    def get_statistics(self):
        return TicketWindowStatistics(self._tickets_sold, self._idle_time)

    def get_window_num(self):
        return self._window_num

    def get_processing_time(self):
        return self._processing_time

    def get_tickets_sold(self):
        return self._tickets_sold

    def is_available(self):
        return self._current_customer is None

    def set_customer(self, customer: Customer):
        if not self.is_available():
            raise Exception("Window is currently OCCUPIED. Cannot set customer")
        else:
            self._current_customer = customer
            self._begin_processing_time = self._clock.get_current_time()

    def increment_idle_time(self):
        self._idle_time += 1

    def update_occupant(self) -> bool:
        ''' Update window occupancy. Returns True if a customer has exited the window, False otherwise '''

        done_processing = self._clock.get_current_time() - self._begin_processing_time == self._processing_time

        if not self.is_available() and done_processing:
            self._tickets_sold += 1
            self._current_customer = None

            return True

        return False


class Theater:
    #Associate each window with lines... Dictionary?

    def __init__(self, num_windows: int, window_configs: dict, line_config: str, clock: Clock):
        #Dictionary - Keys: Window #, Values: Pair - TicketWindow and TicketLine
        assert num_windows > 0
        assert num_windows == len(window_configs)

        self._windows_list = []
        self._lines_list = []
        self._config = line_config
        self._clock = clock

        if line_config == 'S':
            self._lines_list.append(TicketLine(1, clock))

        for window_num in range(1, num_windows + 1):
            self._windows_list.append(TicketWindow(window_num, window_configs[window_num],
                                                   clock))

            if line_config == 'M':
                self._lines_list.append(TicketLine(window_num, clock))

        # Statistics
        self._line_wait_times = []
        self._window_wait_times = []

    def __str__(self):
        result = "--Theater--\n"
        for window in self._windows_list:
            result += str(window) + "\n"

        result += "\n"

        for line in self._lines_list:
            result += str(line) + "\n"

        return result

    def get_all_window_statistics(self) -> {int: TicketWindowStatistics}:
        return {window.get_window_num(): window.get_statistics() for window in self._windows_list}

    def get_all_line_statistics(self) -> {int: TicketLineStatistics}:
        return {line.get_line_num(): line.get_statistics() for line in self._lines_list}

    def get_summary_statistics(self):
        def sum_tickets():
            total_tickets = 0

            for window in self._windows_list:
                total_tickets += window.get_tickets_sold()
            return total_tickets

        return TheaterStatistics(sum_tickets(), self._line_wait_times, self._window_wait_times)

    def take_new_arrival(self, arriving_customer: Customer) -> SimulationEvent:
        sorted_lines = sorted(self._lines_list, key=lambda line: len(line))
        shortest_line = sorted_lines[0]

        shortest_line.enqueue_customer(arriving_customer)
        enter_line_event = CustomerEnterLineEvent(self._clock.get_current_time(),
                                                  shortest_line.get_line_num())
        return enter_line_event

    def update_windows_and_lines(self) -> [SimulationEvent]:
        ''' Performs one update of the theater simulation.
            Update each window, and fill in if necessary
            Returns a list of Events '''

        current_update_log = []

        # Process window updates - update each window's occupancy, and
        # fill in empty windows when needed
        for window in self._windows_list:
            finished_processing_customer = window.update_occupant()

            if finished_processing_customer:
                exit_window_event = CustomerExitWindowEvent(self._clock.get_current_time(),
                                                            window.get_window_num(),
                                                            window.get_processing_time())
                # For keeping track of wall window wait times
                self._window_wait_times.append(window.get_processing_time())
                current_update_log.append(exit_window_event)

            if window.is_available():
                next_customer = self._get_next_customer(window.get_window_num())

                if next_customer is not None:
                    line_num = (window.get_window_num() if self._config == 'M' else 1)
                    exit_line_event = CustomerExitLineEvent(self._clock.get_current_time(),
                                                            line_num,
                                                            next_customer.get_time_spent_in_line())
                    # For keeping track of all customer line wait times
                    self._line_wait_times.append(next_customer.get_time_spent_in_line())
                    current_update_log.append(exit_line_event)

                    window.set_customer(next_customer)
                    enter_window_event = CustomerEnterWindowEvent(self._clock.get_current_time(),
                                                                  window.get_window_num())
                    current_update_log.append(enter_window_event)
                else:
                    window.increment_idle_time()

        for line in self._lines_list:
            line.update_waiting_times()

        return current_update_log

    def _get_next_customer(self, associated_window_num: int):
        # Offset by 1 for the list
        index_num = (associated_window_num if self._config == 'M' else 1) - 1

        if len(self._lines_list[index_num]) > 0:
            return self._lines_list[index_num].dequeue_customer()

        else:
            return None
