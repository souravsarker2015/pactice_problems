class Node:
    def __init__(self, data=None):
        self.data = data
        self.next_node = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.noOfNodes = 0

    def insert_start(self, data):
        self.noOfNodes += 1
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
        else:
            new_node.next_node = self.head
            self.head = new_node

    # linear running time o(n)
    def insert_end(self, data):
        self.noOfNodes += 1
        new_node = Node(data)
        actual_node = self.head

        while actual_node.next_node is not None:
            actual_node = actual_node.next_node

        actual_node.next_node = new_node

    def size_of_linked_list(self):
        return self.noOfNodes

    def delete_node(self, data):
        if self.head is None:
            return
        actual_node = self.head
        previous_node = None

        while actual_node is not None and actual_node.data != data:
            previous_node = actual_node
            actual_node = actual_node.next_node

        if actual_node is None:
            return
        self.noOfNodes -= 1
        if previous_node is None:
            self.head = actual_node.next_node
        else:
            previous_node.next_node = actual_node.next_node

    def traverse_linked_list(self):
        actual_node = self.head

        while actual_node is not None:
            print(actual_node.data)
            actual_node = actual_node.next_node


ll = LinkedList()
ll.insert_start(1)
ll.insert_start(2)
ll.insert_start(3)
ll.insert_start(4)
ll.insert_start(5)

ll.insert_end(15)
ll.insert_end(155)
ll.insert_end(215)

ll.traverse_linked_list()

print('remove:')
ll.delete_node(215)
ll.traverse_linked_list()
