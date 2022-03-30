s = "tadadattaetadadadafa"
len_s = len(s)
sub_string = "dada"
len_sub = len(sub_string)
count = 0
for i in range(len_s):
    n = s[i:i + len_sub]
    if n == sub_string:
        count = count + 1

print(count)
