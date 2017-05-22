class TicketWindowStatistics:
    def __init__(self, num_tickets_sold: int,  idle_time: int):
        self._num_tickets_sold = num_tickets_sold
        self._idle_time = idle_time

    def get_num_tickets_sold(self):
        return self._num_tickets_sold

    def get_idle_time(self):
        return self._idle_time


class TicketLineStatistics:
    def __init__(self, final_length: int, max_length: int, wait_times: [int]):
        self._final_length = final_length
        self._max_length = max_length
        self._wait_times = wait_times

    def get_final_length(self):
        return self._final_length

    def get_max_length(self):
        return self._max_length

    def get_average_wait_time(self):
        if len(self._wait_times) > 0:
            return sum(self._wait_times) / len(self._wait_times)
        else:
            return 0

    def get_max_wait_time(self):
        if len(self._wait_times) > 0:
            return max(self._wait_times)
        else:
            return 0


class TheaterStatistics:
    def __init__(self, total_tickets_sold: int, line_wait_times: [int], window_times: [int]):
        self._total_tickets_sold = total_tickets_sold
        self._line_wait_times = line_wait_times
        self._window_times = window_times

    def get_total_tickets_sold(self):
        return self._total_tickets_sold

    def get_average_line_wait_time(self):
        if len(self._line_wait_times) > 0:
            return sum(self._line_wait_times) / len(self._line_wait_times)
        else:
            return 0

    def get_average_window_time(self):
        if len(self._window_times) > 0:
            return sum(self._window_times) / len(self._window_times)
        else:
            return 0
