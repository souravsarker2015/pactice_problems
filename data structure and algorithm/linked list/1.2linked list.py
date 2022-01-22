class Node:
    def __init__(self, data):
        self.data = data
        self.nextNode = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.noOfNodes = 0

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

        actual_node = self.head

        while actual_node.nextNode is not None:
            actual_node = actual_node.nextNode

        actual_node.nextNode = newNode

    def remove(self, data):
        if self.head is None:
            return

        actual_node = self.head
        previousNode = None

        while actual_node is not None and actual_node.data != data:
            previousNode = actual_node
            actual_node = actual_node.nextNode

        if actual_node is None:
            return

        self.noOfNodes = self.noOfNodes - 1

        if previousNode is None:
            self.head = actual_node.nextNode

        else:
            previousNode.nextNode = actual_node.nextNode

    def size_linked_list(self):
        return self.noOfNodes

    def traverse(self):
        actualNode = self.head
        while actualNode is not None:
            print(actualNode.data)
            actualNode = actualNode.nextNode


linkedList = LinkedList()
linkedList.insert_start(4)
linkedList.insert_start(5)
linkedList.insert_end(15)
linkedList.insert_end(112)

linkedList.traverse()
print(linkedList.size_linked_list())
linkedList.remove(15)
linkedList.traverse()
print(linkedList.size_linked_list())
