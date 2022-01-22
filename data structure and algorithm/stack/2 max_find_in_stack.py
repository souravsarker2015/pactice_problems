class Stack:
    def __init__(self):
        self.max_stack = []
        self.main_stack = []

    def insert(self, data):
        self.main_stack.append(data)

        if len(self.main_stack) == 1:
            self.max_stack.append(data)

        if data >= (self.max_stack[-1]):
            self.max_stack.append(data)
        else:
            self.max_stack.append(self.max_stack[-1])

    def pop(self):
        self.max_stack.pop()
        return self.main_stack.pop()

    def get_max(self):
        return self.max_stack.pop()


if __name__ == "__main__":
    stack = Stack()
    stack.insert(1)
    stack.insert(100)
    stack.insert(150)
    stack.insert(2)

    print(stack.get_max())
