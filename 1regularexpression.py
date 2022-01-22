# import re
#
# pattern=r'color'
#
# # if re.match(pattern,'My shirt color is red color'):
# # if re.search(pattern,'My shirt color is red color'):
# #     print('Match')
# # else:
# #     print('Not Match')
# match=re.search(pattern,'My shirt color is red color')
# if match:
#     print(match.start())
#     print(match.end())
#     print(match.span())
#
# # print(re.search(pattern,'My shirt color is red color'))

# import re
# test_text="123bikrom@007 family_banglamotor engineer scholar person23341 in bangladess"
#
# match=re.finditer(r'engineer',test_text)
#
# print(match)
# import re
# test_text="123bikrom@007 family_banglamotor engineer scholar person23341 in bangladess"
# pattern=re.compile(r"007")
# # match=re.finditer(r'engineer',test_text)
# matches= pattern.finditer(test_text)
# for match in matches:
#     print(match)
###################################################

# import re
# test_text="123bikrom@007 family_banglamotor engineer scholar person233417 in bangladess"
#
# # pattern=re.compile(r"bikrom")
# pattern=re.compile(r"123")
# matches=pattern.match(test_text)
#
# print(matches)
# # for match in matches:
# #     print(match)

# import re
# test_text="123bikrom@007 family_banglamotor .engineer scholar person233417 in bangladess"
#
# # pattern=re.compile(r"bikrom")
# pattern=re.compile(r"2")
# matches=pattern.finditer(test_text)
#
# for matches in matches:
#     print(matches.group(), "\n",matches.start(), "\n",matches.end(),"\n",matches.span() )
#

import re
test_text="22-03-1999 , 22_03_99, 22_03_99"
pattern=re.compile(r"\d{2}[-_]\d{2}[-_]\d{2,4}")
matches=pattern.finditer(test_text)
for matches in matches:
    print(matches)









