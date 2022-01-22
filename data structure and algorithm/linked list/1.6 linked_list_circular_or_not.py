class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None


def circular(head):
    if head == None:
        return True
    node = head.next
    #i = 0
    while node is not None and node is not head:
        #i = i + 1
        node = node.next
    return (node == head)


if __name__ == "__main__":
    llist = LinkedList()
    llist.head = Node(1)
    second = Node(2)
    third = Node(3)
    fourth = Node(4)

    llist.head.next = second
    second.next = third
    third.next = fourth

    if circular(llist.head):
        print("Yes")
    else:
        print("No")

    fourth.next = llist.head
    if circular(llist.head):
        print("yes")
    else:
        print("no")
