class Queue:
    def __init__(self):
        self.enqueue_list = []
        self.dequeue_list = []

    def enqueue(self, data):
        self.enqueue_list.append(data)

    def dequeue(self):
        if self.enqueue_list == [] and self.dequeue_list == []:
            raise Exception("List is empty")

        while len(self.enqueue_list) != 0:
            self.dequeue_list.append(self.enqueue_list.pop())
        return self.dequeue_list.pop()


if __name__ == "__main__":
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.enqueue(4)
    print(queue.dequeue())
    # for i in range(5):
    #     queue.enqueue(i)
    # # print(queue.enqueue())
    #

    print(queue.dequeue())
