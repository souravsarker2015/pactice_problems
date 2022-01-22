punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
m = 'somir is good boy!!!--{{('
n = ""
for i in m:
    if i not in punctuations:
        n = n + i

print(n)
