class Node:
    def __init__(self, data):
        self.data = data
        self.nextNode = None
        self.previousNode = None


class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, data):
        newNode = Node(data)
        if self.head is None:
            self.head = newNode
            self.tail = newNode

        else:
            newNode.previousNode = self.tail
            self.tail.nextNode = newNode
            self.tail = newNode

    def traverse_forward(self):
        actualNode = self.head
        while actualNode is not None:
            print(actualNode.data)
            actualNode = actualNode.nextNode

    def traverse_backword(self):
        actualNode = self.tail

        while actualNode is not None:
            print(actualNode.data)
            actualNode = actualNode.previousNode


double_linked_list = DoubleLinkedList()
double_linked_list.insert(1)
double_linked_list.insert(2)
double_linked_list.insert(3)
double_linked_list.insert(4)
double_linked_list.traverse_forward()
print("_______________________")
double_linked_list.traverse_backword()
