def add(n1, n2):
    return n1 + n2


def sub(n1, n2):
    return n1 - n2


def mul(n1, n2):
    return n1 * n2


def div(n1, n2):
    return n1 / n2


print("Select Operation: ")
while True:
    choice = input("choice (+ - * /) : ")
    if choice in ('+', '-', '*', '/'):
        n1 = float(input("Enter one Number : "))
        n2 = float(input("Enter another Number : "))

        if choice == '+':
            print(f"Summation = {add(n1, n2)}")

        elif choice == '-':
            print(f"Subtraction = {sub(n1, n2)}")

        elif choice == '*':
            print(f"Multiplication = {mul(n1, n2)}")

        elif choice == '/':
            print(f"Division = {div(n1, n2)}")

        next_calculation = input("Another calculation (yes/no) :")
        if next_calculation == 'no':
            break
        else:
            continue
    else:
        print("Invalid Input")
