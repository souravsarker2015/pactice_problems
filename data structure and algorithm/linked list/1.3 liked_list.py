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

        actualNode = self.head

        while actualNode.nextNode is not None:
            actualNode = actualNode.nextNode

        actualNode.nextNode = newNode

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

    def travers(self):
        actualNode = self.head
        while actualNode is not None:
            print(actualNode.data)
            actualNode = actualNode.nextNode

    def sizeOfNode(self):
        return self.noOfNodes


linked_list = LinkedList()
linked_list.insert_start(5)
linked_list.insert_start(5)
linked_list.insert_start(5)
linked_list.insert_start(5)
linked_list.insert_end(10)
linked_list.insert_end(10)
linked_list.travers()

print(linked_list.sizeOfNode())
print("________")
linked_list.remove(10)
linked_list.travers()
print(linked_list.sizeOfNode())

