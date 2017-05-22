class SimulationEvent:
    def __init__(self, time: int, message='An event has occurred'):
        self._time = time
        self._message = message

    def get_formatted_log_message(self) -> str:
        return 'Time    {} - {}'.format(self._time, self._message)


class CustomerLineEvent(SimulationEvent):
    def __init__(self, time: int, line_num: int):
        SimulationEvent.__init__(self, time)
        self._line_num = line_num
        self._message = 'A customer event has occurred at Line #{}'.format(line_num)


class CustomerEnterLineEvent(CustomerLineEvent):
    def __init__(self, time: int, line_num: int):
        CustomerLineEvent.__init__(self, time, line_num)
        self._message = 'Customer entered line #{}'.format(line_num)


class CustomerExitLineEvent(CustomerLineEvent):
    def __init__(self, time: int, line_num: int, waiting_time: int):
        CustomerLineEvent.__init__(self, time, line_num)
        self._message = 'Customer exited line #{} (spent {} seconds in line)'.format(line_num, waiting_time)


class CustomerWindowEvent(SimulationEvent):
    def __init__(self, time: int, window_num: int):
        SimulationEvent.__init__(self, time)
        self._window_num = window_num
        self._message = 'A customer event has occurred at Window #{}'.format(window_num)


class CustomerEnterWindowEvent(CustomerWindowEvent):
    def __init__(self, time: int, window_num: int):
        CustomerWindowEvent.__init__(self, time, window_num)
        self._message = 'Customer entered window #{}'.format(window_num)


class CustomerExitWindowEvent(CustomerWindowEvent):
    def __init__(self, time: int, window_num: int, process_time: int):
        CustomerWindowEvent.__init__(self, time, window_num)
        self._message = 'Customer exited window #{} (spent {} seconds at window)'.format(window_num, process_time)