# Node and LinkedList classes


class Node:
    def __init__(self, value = None, next = None, previous = None):
        self.value = value
        self.next = next
        self.previous = previous

    def __str__(self):
        return str(self.value)

    def print_linked(self):
        return str(self.value) + '->' + str(self.next)


class LinkedList:
    def __init__(self):
        self._head = self._tail = None
        self._length = 0

    def append(self, item):
        if self._head is None:
            new_node = Node(item)
            self._head = new_node
            self._tail = new_node
        else:
            new_node = Node(item, None, self._tail)
            self._tail.next = new_node
            self._tail = new_node

        self._length += 1

    def prepend(self, item):
        new_node = Node(item, self._head)
        self._head = new_node
        self._length += 1

    def remove_first(self):
        if self._head is not None:
            self._head = self._head.next
            self._length -= 1
        else:
            raise IndexError('Remove from empty list')

    def remove_last(self):
        if self._tail is not None:
            self._tail.previous = None
            self._length -= 1
        else:
            raise IndexError('Remove from empty list')

    def __str__(self):
        if self._length == 0:
            return '[]'

        result = '['

        for value in self:
            result += "{}, ".format(value)

        return result[:-2] + ']'

    def __len__(self):
        return self._length

    def _getnode_at_index(self, index):
        if type(index) is not int:
            raise IndexError("Index must be int, not {}".format(type(index)))

        if index < 0:
            index += self._length

        if not 0 <= index < self._length:
            raise IndexError("Out of bounds")

        elif index <= self._length // 2:
            current_index = 0
            current_node = self._head

            while current_node is not None and current_index < index:
                current_node = current_node.next
                current_index += 1

            return current_node

        else:
            current_index = self._length - 1
            current_node = self._tail

            while current_node is not None and current_index > index:
                current_node = current_node.previous
                current_index -= 1

            return current_node


    def __getitem__(self, index):
        if type(index) is slice:
            result = LinkedList()

            positive_start_index = self._length + index.start if index.start < 0 else index.start
            positive_end_index = self._length + index.stop if index.stop < 0 else index.stop

            for i in range(positive_start_index, positive_end_index):
                result.append(self[i])

            return result
        else:
            node_at_index = self._getnode_at_index(index)
            return node_at_index.value

    def __setitem__(self, index, value):
        node_at_index = self._getnode_at_index(index)
        node_at_index.value = value

    def __delitem__(self, index):
        if type(index) is slice:
            positive_start_index = self._length + index.start if index.start < 0 else index.start
            positive_end_index = -1 + (self._length + index.stop if index.stop < 0 else index.stop)

            for i in range(positive_end_index, positive_start_index - 1, -1):
                del self[i]

        else:
            current_node = self._getnode_at_index(index)
            current_node.previous.next = current_node.next
            current_node.next.previous = current_node.previous

            self._length -= 1

    def __iter__(self):
        current_node = self._head

        while current_node is not None:
            yield current_node.value
            current_node = current_node.next
