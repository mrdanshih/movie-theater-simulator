from file_reader import FileReader
from theater_components import Theater
from clock import Clock
from customer import Customer
from simulation_events import SimulationEvent

# Simulation class

class Simulation:
    def __init__(self, input_file: str):
        self._my_file_reader = iter(FileReader(input_file))
        self._initialize_attributes()

    def _initialize_attributes(self):
        self._clock = Clock()
        self._name = next(self._my_file_reader)
        self._total_simulation_time = 60 * int(next(self._my_file_reader))

        num_windows = int(next(self._my_file_reader))
        line_config = next(self._my_file_reader)

        window_configs = dict()

        for i in range(num_windows):
            window_configs[i + 1] = int(next(self._my_file_reader))

        self._theater = Theater(num_windows, window_configs, line_config, self._clock)

    def run_simulation(self):
        print(SimulationEvent(0, 'Simulation started').get_formatted_log_message())

        self._simulate_theater()

        print(SimulationEvent(self._total_simulation_time, 'Simulation ended').get_formatted_log_message())
        print()
        self._print_simulation_statistics()

    def _simulate_theater(self):
        next_batch_of_customers, arrival_time = self._get_next_customer_batch()

        while self._clock.get_current_time() < self._total_simulation_time:
            events_this_second = []

            if next_batch_of_customers is not None and self._clock.get_current_time() == arrival_time:
                for customer in next_batch_of_customers:
                    line_arrival_event = self._theater.take_new_arrival(customer)
                    events_this_second.append(line_arrival_event)

                next_batch_of_customers, arrival_time = self._get_next_customer_batch()

            window_and_line_events = self._theater.update_windows_and_lines()
            events_this_second.extend(window_and_line_events)
            self._print_all_events(events_this_second)

            self._clock.increment()

    def _print_simulation_statistics(self):
        print('--- Simulation Statistics ---')
        all_window_statistics_dict = self._theater.get_all_window_statistics()
        all_line_statistics_dict = self._theater.get_all_line_statistics()
        theater_summary_stats = self._theater.get_summary_statistics()

        for window_num, window_stats in all_window_statistics_dict.items():
            print('Window #{}'.format(window_num))
            print('\tTickets sold: {}'.format(window_stats.get_num_tickets_sold()))
            idle_fraction = window_stats.get_idle_time() / self._total_simulation_time
            print('\tIdle time: {:.2f}% ({} seconds out of {})'.format(100 * idle_fraction,
                                                                      window_stats.get_idle_time(),
                                                                      self._total_simulation_time))

        for line_num, line_stats in all_line_statistics_dict.items():
            print('Line #{}'.format(line_num))
            print('\tCustomers waiting at simulation end: {}'.format(line_stats.get_final_length()))
            print('\tMaximum length: {} customers'.format(line_stats.get_max_length()))
            print('\tAverage wait time: {:.2f} seconds'.format(line_stats.get_average_wait_time()))
            print('\tMaximum wait time: {} seconds'.format(line_stats.get_max_wait_time()))

        print('Overall')
        print('\tTickets sold: {}'.format(theater_summary_stats.get_total_tickets_sold()))
        print('\tAverage wait time: {:.2f} seconds'.format(theater_summary_stats.get_average_line_wait_time()))
        print('\tAverage time spent at a window: {:.2f} seconds'.format(theater_summary_stats.get_average_window_time()))

    def _print_all_events(self, events: [SimulationEvent]) -> None:
        for event in events:
            print(event.get_formatted_log_message())

    def _get_next_customer_batch(self) -> ([Customer], int):
        next_batch = next(self._my_file_reader).strip()

        if next_batch == 'END':
            return None, None
        else:
            tokens = next_batch.split()
            num_customers, arrival_time = int(tokens[0]), int(tokens[1])

            return self._create_customer_list(num_customers), arrival_time

    def _create_customer_list(self, num_customers: int) -> [Customer]:
        return [Customer() for num in range(num_customers)]

if __name__ == '__main__':
    x = Simulation('simulation.txt')
    x.run_simulation()









