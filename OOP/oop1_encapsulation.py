class MyClass(object):
    def __init__(self):
        self.value = None

    def set_val(self, val):
        self.value = val

    def get_val(self):
        return self.value


i = MyClass()
i.value = 10
print(i.get_val())
j = MyClass()
j.value = 10
print(j.get_val())
