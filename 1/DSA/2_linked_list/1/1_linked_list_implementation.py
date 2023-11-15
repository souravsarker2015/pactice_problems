class Node:
    def __init__(self, data=None):
        self.data = data
        self.next_node = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.no_of_nodes = 0

    def insert_start(self, data):
        self.no_of_nodes += 1
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
        else:
            new_node.next_node = self.head
            self.head = new_node

    def insert_end(self, data):
        self.no_of_nodes += 1
        actual_node = self.head
        new_node = Node(data)
        while actual_node.next_node is not None:
            actual_node = actual_node.next_node

        actual_node.next_node = new_node

    def delete_node(self, data):
        if self.head is None:
            return

        actual_node = self.head
        previous_node = None

        while actual_node is not None and actual_node.data != data:
            previous_node = actual_node
            actual_node = actual_node.next_node

        self.no_of_nodes -= 1

        if previous_node is None:
            self.head = actual_node.next_node
        else:
            previous_node.next_node = actual_node.next_node

    def traverse_linked_list(self):
        actual_node = self.head

        while actual_node is not None:
            print(actual_node.data)
            actual_node = actual_node.next_node


if __name__ == "__main__":
    linked_list = LinkedList()
    linked_list.insert_start(0)
    linked_list.insert_start(1)
    linked_list.insert_start(2)
    linked_list.insert_end(5)
    linked_list.delete_node(5)
    linked_list.traverse_linked_list()
