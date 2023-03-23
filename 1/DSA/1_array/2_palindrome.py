# string / array is palindrome or not
import math


def rev_str(name_input):
    name_input = list(name_input)

    startIndex = 0
    endIndex = len(name_input) - 1
    print(startIndex)
    print(endIndex)
    for i in range(math.ceil(len(name_input)/2)):
        if startIndex != endIndex:
            name_input[startIndex] = name_input[endIndex]
            name_input[endIndex] = name_input[startIndex]
    #     pass
    # while endIndex > startIndex:
    #     name_input[startIndex] = name_input[endIndex]
    #     name_input[endIndex] = name_input[startIndex]
    print(name_input)
    return ''.join(name_input)


def is_palindrome(name):
    rev_name = rev_str(name)

    # print(name[::-1])
    if name == rev_name:
        print("palindrome")
    else:
        print("not palindrome")


if __name__ == '__main__':
    input_str = input("Enter a input : ")
    is_palindrome(input_str)
