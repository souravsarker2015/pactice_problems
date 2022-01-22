def name():
    return 'john', 'bikrom'


print(name())
n1, n2 = name()
print(n1, n2)


def name1():
    n1 = 'john'
    n2 = 'bikrom'

    return {1: n1, 2: n2}


print(name1())
