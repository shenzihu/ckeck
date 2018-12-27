import re
num = (1,2,3)
n1,n2,n3 = num
print n1
print n2
print """ 's'dasdsds"ddd"d"""
ip = "172.1.0.1"
pattern = re.compile(ur'(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})(\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})){3}')
print(pattern.match(ip).span())