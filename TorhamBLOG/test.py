import random
char="qwertyuioplkjhgfdsazxcvbnm1234567890QWERTYUIOPLKJHGFDSAZXCVBNM"


print(char[1])

char_set = ''
for i in range(0,70):
	str_random = random.randrange(0,62)
	char_set += char[str_random]


print(char_set)