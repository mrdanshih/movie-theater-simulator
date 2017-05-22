from queue33 import *
import unittest

class QueueTests(unittest.TestCase):
    def test_enqueue(self):
        q = Queue()
        q.enqueue(3)
        self.assertEquals(q.front(), 3)
        self.assertEquals(len(q), 1)


    def test_dequeue(self):
        q = self._build_queue_with_elements()

        for i in range(10):
            self.assertEquals(q.dequeue(), i)
        self.assertEquals(len(q), 0)

    def test_iteration_is_supported(self):
        q = self._build_queue_with_elements()
        self.assertEquals(list(q), [i for i in range(10)])


    def _build_queue_with_elements(self):
        x = Queue()
        for i in range(10):
            x.enqueue(i)
        return x
        
