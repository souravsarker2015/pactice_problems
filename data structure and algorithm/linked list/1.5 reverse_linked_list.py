class Node:
    def __init__(self, data):
        self.data = data
        self.nextNode = None


class LinkedList:
    def __init__(self):
        self.noOfNodes = 0
        self.head = None

    def insert_start(self, data):
        self.noOfNodes = self.noOfNodes + 1
        newNode = Node(data)

        if not self.head:
            self.head = newNode

        else:
            newNode.nextNode = self.head
            self.head = newNode

    def insert_end(self, data):
        self.noOfNodes = self.noOfNodes + 1
        newNode = Node(data)

        actualNode = self.head

        while actualNode.nextNode is not None:
            actualNode = actualNode.nextNode

        actualNode.nextNode = newNode

    def middle(self):
        fast_pointer = self.head
        slow_pointer = self.head

        while fast_pointer.nextNode and fast_pointer.nextNode.nextNode:
            fast_pointer = fast_pointer.nextNode.nextNode
            slow_pointer = slow_pointer.nextNode

        return slow_pointer

    def reverse(self):
        current_node = self.head
        previousNode = None
        nextNode = None

        while current_node is not None:
            nextNode = current_node.nextNode
            current_node.nextNode = previousNode
            previousNode = current_node
            current_node = nextNode

        self.head = previousNode

    def remove(self, data):
        if self.head is None:
            return

        actualNode = self.head
        previousNode = None

        while actualNode is not None and actualNode.data != data:
            previousNode = actualNode
            actualNode = actualNode.nextNode

        if actualNode is None:
            return
        self.noOfNodes = self.noOfNodes - 1
        if previousNode is None:
            self.head = actualNode.nextNode

        else:
            previousNode.nextNode = actualNode.nextNode

    def size_of_node(self):
        return self.noOfNodes

    def traverse(self):
        actualNode = self.head
        while actualNode is not None:
            print(actualNode.data)
            actualNode = actualNode.nextNode


linked_list = LinkedList()

linked_list.insert_start(1)
linked_list.insert_start(2)
linked_list.insert_start(3)
linked_list.insert_start(4)
linked_list.insert_end(10)
linked_list.traverse()
print(f"middle element : {linked_list.middle().data}")
linked_list.reverse()
linked_list.traverse()
