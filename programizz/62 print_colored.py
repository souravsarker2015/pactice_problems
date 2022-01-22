from termcolor import colored
from dateutil import parser

print(colored('pr', 'blue'))

date = parser.parse("Mar 11 2011 11:31AM")
print(date)
date = parser.parse("11 Mar 2011 11:31AM")
print(colored(date, 'red'))

# 64 last element in a list
n = ['a', 'b', 'c', 'd', 'e']
print(n[1:4:1])
