class Queue:
    def __init__(self):
        self.stack = []

    def enqueue(self, data):
        self.stack.append(data)

    def dequeue(self):
        if len(self.stack) == 1:
            return self.stack.pop()

        item = self.stack.pop
        dequeue_items = self.dequeue()
        self.stack.append(item)
        return dequeue_items


queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(queue.dequeue())
print(queue.dequeue())
print(queue.dequeue())
