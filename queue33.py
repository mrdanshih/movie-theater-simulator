from linkedlist33 import *

# Queue class

class QueueEmptyException(Exception):
    pass


class Queue:
    def __init__(self):
        self._internal_queue = LinkedList()

    def enqueue(self, item):
        self._internal_queue.append(item)

    def dequeue(self):
        first_item = self.front()
        self._internal_queue.remove_first()
        return first_item

    def front(self):
        if len(self._internal_queue) == 0:
            raise QueueEmptyException('Queue is empty')

        return self._internal_queue[0]

    def __len__(self):
        return len(self._internal_queue)

    def __iter__(self):
        return iter(self._internal_queue)



