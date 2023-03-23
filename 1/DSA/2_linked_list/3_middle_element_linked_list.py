class Node:
    def __init__(self, data):
        self.data = data
        self.next_node = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.no_of_nodes = 0

    def insert_first(self, data):
        self.no_of_nodes += 1
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
        else:
            new_node.next_node = self.head
            self.head = new_node

    def middle_element(self):
        slow_pointer = self.head
        fast_pointer = self.head

        while fast_pointer.next_node is not None and fast_pointer.next_node.next_node is not None:
            fast_pointer = fast_pointer.next_node.next_node
            slow_pointer = slow_pointer.next_node

        return slow_pointer


ll = LinkedList()
ll.insert_first(1)
ll.insert_first(2)
ll.insert_first(3)
ll.insert_first(4)
print(ll.middle_element().data)
