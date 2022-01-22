class Stack:
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if len(self.stack) < 1:
            return -1

        data = self.stack[-1]
        del self.stack[-1]
        return data

    def peek(self):
        return self.stack[-1]

    def size_stack(self):
        return len(self.stack)

    def is_empty(self):
        return self.stack == []

stack=Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(f"Popped item : {stack.pop()}")
print(f"size of stack : {stack.size_stack()}")
print(f"peeked item : {stack.peek()}")
print(f"size of stack : {stack.size_stack()}")

