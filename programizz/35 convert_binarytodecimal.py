def convert_binary_to_decimal(dec):
    if dec > 1:
        convert_binary_to_decimal(dec // 2)
    print(dec % 2, end=" ")


dec = 34
convert_binary_to_decimal(dec)
