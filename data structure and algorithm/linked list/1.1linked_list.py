class Node:
    def __init__(self, data):
        self.data = data
        self.nextNode = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.numberOfNode = 0

    def insert_start(self, data):
        self.numberOfNode = self.numberOfNode + 1
        newNode = Node(data)

        if not self.head:
            self.head = newNode

        else:
            newNode.nextNode = self.head
            self.head = newNode

    def insert_end(self, data):
        self.numberOfNode = self.numberOfNode + 1
        newNode = Node(data)

        actualNode = self.head
        while actualNode.nextNode is not None:
            actualNode = actualNode.nextNode
        actualNode.nextNode = newNode

    def size_linkedList(self):
        return self.numberOfNode

    def remove(self, data):
        if self.head is None:
            return

        actual_node = self.head
        previous_node = None

        while actual_node is not None and actual_node.data != data:
            previous_node = actual_node
            actual_node = actual_node.nextNode

        if actual_node is None:
            return
        self.numberOfNode = self.numberOfNode - 1

        if previous_node is None:
            self.head = actual_node.nextNode
        else:
            previous_node.nextNode = actual_node.nextNode

    def traverse(self):
        actualNode = self.head
        while actualNode is not None:
            print(actualNode.data)
            actualNode = actualNode.nextNode


linklist = LinkedList()
linklist.insert_start(4)
linklist.insert_start(5)
linklist.insert_end(10)
linklist.remove(10)
linklist.traverse()

# class Node:
#     def __init__(self, data):
#         self.data = data
#         self.nextNode = None
#
#
# class LinkedList:
#     def __init__(self):
#         self.numOfNodes = 0
#         self.head = None
#
#     def insert(self, data):
#         self.numOfNodes = self.numOfNodes + 1
#         newNode = Node(data)
#         if not self.head:
#             self.head = newNode
#
#         else:
#             newNode.nextNode = self.head
#             self.head = newNode


# class Node:
#     def __init__(self, data):
#         self.data = data
#         self.nextNode = None
#
#
# class LinkedList:
#     def __init__(self):
#         self.head = None
#         self.numberOfNode = 0
#
#     def insert_start(self, data):
#         self.numberOfNode = self.numberOfNode + 1
#         newNode = Node(data)
#
#         if not self.head:
#             self.head = newNode
#
#         else:
#             newNode.nextNode = self.head
#             self.head = newNode
#
#     def insert_end(self, data):
#         self.numberOfNode = self.numberOfNode + 1
#         newNode = Node(data)
#
#         actual_node = self.head
#
#         while actual_node.nextNode is not None:
#             actual_node = actual_node.nextNode
#
#         actual_node.nextNode = newNode
#
#     def sizeLinkedList(self):
#         return self.numberOfNode
#
#     def removeNode(self, data):
#         if self.head is None:
#             return
#
#         actual_node = self.head
#         previous_node = None
#
#         while actual_node.nextNode is not None and actual_node.data != data:
#             previous_node = actual_node
#             actual_node = actual_node.nextNode
#
#         if actual_node is None:
#             return
#
#         if previous_node is None:
#             self.head = actual_node.nextNode
#
#         else:
#             previous_node.nextNode = actual_node.nextNode
#
#     def traverse(self):
#
#         actual_node = self.head
#         while actual_node is not None:
#             print(actual_node.data)
#             actual_node = actual_node.nextNode
#

# linklist = LinkedList()
# linklist.insert_start(4)
# linklist.insert_start(5)
# linklist.insert_end(10)
# linklist.removeNode(10)
# linklist.traverse()
