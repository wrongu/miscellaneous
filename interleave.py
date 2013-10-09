from random import random

x = "10101101"
y = "0010110111"
n = 100
# 'next' index into x and y, cycling back to 0
xi = yi = 0
z = '' # z = x~y (interleave)
source = '' # the "answers" of which digit came from which source

for i in range(n):
	if(random() < 0.5):
		# take from x
		z += x[xi]
		source += 'x'
		xi = (xi+1) % len(x)
	else:
		# take from y
		z += y[yi]
		source += 'y'
		yi = (yi+1) % len(y)

if __name__ == "__main__":
	print "X:", x
	print "Y:", y
	print "Z:", z
	print "  ", source
