from linkedlist33 import *
import unittest

class LinkedListTests(unittest.TestCase):
    def test_append(self):
        x = LinkedList()
        x.append(1)
        self.assertEquals(x._head.value, 1)
        x.append(2)
        self.assertEquals(x._head.next.value, 2)
        x.append(3)
        self.assertEquals(x._head.next.next.value, 3)

    def test_prepend(self):
        x = LinkedList()
        x.prepend(1)
        self.assertEquals(x._head.value, 1)
        x.prepend(2)
        self.assertEquals(x._head.next.value, 1)
        self.assertEquals(x._head.value, 2)
        x.prepend(5)
        self.assertEquals(x._head.next.next.value, 1)
        self.assertEquals(x._head.next.value, 2)
        self.assertEquals(x._head.value, 5)

    def test_remove_first(self):
        x = self._build_list_with_elements()
        self.assertEquals(x._head.value, 0)
        x.remove_first()
        self.assertEquals(x._head.value, 1)


    def test_getitem(self):
        x = self._build_list_with_elements()

        for i in range(10):
            self.assertEquals(x[i], i)

        self.assertEquals(x[9], 9)
        self.assertEquals(x[-1], 9)
        self.assertEquals(x[-5], 5)

    def test_getslice(self):
        x = self._build_list_with_elements()
        y = [i for i in range(10)]

        self.assertEquals(list(x[3:6]), y[3:6])
        self.assertEquals(list(x[-3:2]), y[-3:2])
        self.assertEquals(list(x[-5:10]), y[-5:10])

    def test_getitem_out_of_bounds(self):
        x = LinkedList()
        self.assertRaises(IndexError, lambda: x[0])
        self.assertRaises(IndexError, lambda: x[-1])

        x = self._build_list_with_elements()
        self.assertRaises(IndexError, lambda: x[-100])


    def test_setter(self):
        x = self._build_list_with_elements()

        x[5] = -99
        self.assertEquals(x[5], -99)
        x[0] = x[9]
        self.assertEquals(x[0], 9)

    def test_del(self):
        x = self._build_list_with_elements()
        y = [i for i in range(10)]

        for i in range(8, 1, -1):
            del x[i]
            del y[i]
            self.assertEquals(list(x), y)

    def test_delslice(self):
        x = self._build_list_with_elements()
        y = [i for i in range(10)]
        del x[2:8]
        del y[2:8]
        self.assertEquals(list(x), y)

    def test_iterator(self):
        x = self._build_list_with_elements()
        y = list(x)
        self.assertEquals(y, [i for i in range(10)])

        comparison_value = 0

        for value in x:
            self.assertEquals(value, comparison_value)
            comparison_value += 1


    def _build_list_with_elements(self):
        x = LinkedList()
        for i in range(10):
            x.append(i)
        return x

if __name__ == '__main__':
    unittest.main(exit = False)