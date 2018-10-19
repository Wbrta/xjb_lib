#!/bin/python

import math
import random

big_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
small_char = "abcdefghijklmnopqrstuvwxyz"
number = "1234567890"
other = "!$#%"

weight_big_char = 0.4
weight_small_char = 0.4
weight_number = 0.15
weight_other = 0.06

length = random.choice(range(10, 30))
num_other = math.ceil(weight_other * length)
num_number = math.ceil(weight_number * length)
num_small_char = math.ceil(weight_small_char * length)
num_big_char = length - num_other - num_number - num_small_char

passwd = [random.choice(big_char) for _ in range(num_big_char)]
passwd.extend([random.choice(small_char) for _ in range(num_small_char)])
passwd.extend([random.choice(number) for _ in range(num_number)])
passwd.extend([random.choice(other) for _ in range(num_other)])

random.shuffle(passwd)
print ("".join(passwd))