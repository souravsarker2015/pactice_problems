st = input()

try:
    n = int(input())
    new = st + n
    print(new)
except (TypeError, ValueError) as e:
    print(e)
