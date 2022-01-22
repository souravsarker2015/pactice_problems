n = int(input("Enter a number :"))

if n % 4 == 0:
    if n % 100 == 0:
        if n % 400 == 0:
            print("Leap Year")
        else:
            print("Not Leap Year")
    else:
        print("Leap Year")

else:
    print("Not Leap Year")