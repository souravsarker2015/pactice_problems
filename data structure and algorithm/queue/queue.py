class Queue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return self.queue == []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        if len(self.queue) < 1:
            return -1

        data = self.queue[0]
        del self.queue[0]
        return data

    def peek(self):
        return self.queue[0]

    def size_queue(self):
        return len(self.queue)


if __name__ == "__main__":
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    print(f"size of queue : {queue.size_queue()}")
    print(f"Dequeue : {queue.dequeue()}")
    print(f"size of queue : {queue.size_queue()}")
    print(f"peek : {queue.peek()}")
