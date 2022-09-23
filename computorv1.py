import sys

def verifyDegree(s):
	if not s[2:].isnumeric():
		print("Error:\nThe degree of X should be a number")
		exit()
	return int(s[2:])

def verifyArg(i):
	b2o = isNumOrFloat(i)
	if (i.find("X^") != -1):
		verifyDegree(i)
		b2o = True
	if (i == '=' or i == '+' or i == '-' or i == '*'):
		b2o = True
	if b2o == False:
		print("Error\nInvalid Equation")
		exit()

def isNumOrFloat(s):
	ap = False
	b2o = False
	for x in s:
		b2o = True
		if not x.isdigit():
			if x == chr(ord('.')) and ap == True:
				b2o = False
				break
			elif x == chr(ord('.')):
				ap = True
			else:
				b2o = False
				break
	if s and (s[0] == '.' or s[len(s) - 1] == '.' or (len(s) >= 2 and s[0] == '0' and s[1] != '.')):
		b2o = False
	return b2o

def listOrder(l):
	status = 1
	# status = 0 : +
	# status = 1 : Num
	# status = 2 : '*'
	# status = 3 : X^num
	isFirst = True
	ok = True
	hasPassed = False
	for i in range(len(l)):
		if (status == 0):
			if (l[i] == '='):
				isFirst = True
				hasPassed=True
				status += 1
				continue
			status = 1
			if l[i] != '+' and l[i] != '-':
				ok = False
				break
		elif (status == 1):
			if (isFirst and hasPassed == False):
				isFirst = False
				if l[i] == '+' or l[i] == '-':
					continue
			if not isNumOrFloat(l[i]):
				ok = False
				break
			else:
				if (isFirst and hasPassed):
					isFirst=False
			status+=1
		elif (status == 2):
			if l[i] != '*':
				ok = False
				break
			status+=1
		elif (status == 3):
			if (l[i].find("X^") != -1):
				verifyDegree(l[i])
				status = 0
			else:
				ok = False
				break
	if ok == False or isFirst==True or hasPassed==False:
		print("Error\nInvalid equation")
		exit()

def listToTrucate(l):
	neg = False
	eq = False
	l2 = list()
	for i in l:
		if i == '-':
			neg = True if eq == False else False
		elif i == '+':
			neg = False if eq == False else True
		elif i == '=':
			eq = True
			neg = True
		elif isNumOrFloat(i):
			f = float(i)
			if (neg == True):
				f *= -1
			l2.append(f)
		elif (i.find("X^") != -1):
			l2.append(verifyDegree(i))
	return(l2)


def simplifyList(l):
	i = -1
	while i < len(l):
		i+=1
		if i % 2 == 1:
			ll = 0
			while ll < len(l):
				if ll % 2 == 0 or ll == i:
					ll+=1
					continue
				if (l[ll] == l[i]):
					l[i - 1] += l[ll-1]
					l.pop(ll)
					l.pop(ll - 1)
				ll+=1
	return l


def parseArg(s):
	l = s.split(' ')
	for i in l:
		verifyArg(i)
	listOrder(l)
	return listToTrucate(l)

def printReduced(l):
	j = -1
	print("Reduced form: ", end='')
	for i in l:
		j += 1
		print(abs(int(i)) if j % 2 == 0 and i.is_integer() else abs(i), end=' ')
		if (j % 2 == 0):
			print("* X^", end='')
		if (j % 2 == 1):
			print('+ ' if len(l) > j + 1 and l[j + 1] > 0 else('- ' if len(l) > j + 1 else ''), end='')
	print('= 0')

def printDegree(l):
	deg = list({})
	b2o = False
	for i in range(len(l)):
		if (i % 2 == 1):
			deg.append(l[i])
			if(l[i] == 0 and l[i - 1] == 0):
				b2o = True
	if len(deg) == 0:
		print("Error\nInvalid Equation")
		exit()
	print("Polynomial degree:", max(deg))
	if max(deg) == 0 and b2o == True:
		print("The polynomial degree is strictly equal to 0 and no solution are found, so each real number is a solution...")
		exit()
	return max(deg)

def resolveFirst(l):
	for i in range(len(l)):
		if (i % 2 == 1):
			if l[i] == 1:
				s = l[i - 1]
			if l[i] == 0:
				f = l[i - 1]
	return f / s * -1

def resolveSecond(l):
	for i in range(len(l)):
		if (i % 2 == 1):
			if l[i] == 1:
				b = l[i - 1]
			if l[i] == 0:
				c = l[i - 1]
			if l[i] == 2:
				a = l[i - 1]
	delta = (b*b) - (4 * (a * c))
	if delta < 0:
		print("Discriminant is strictly negative, I can't solve.")
		exit()
	if delta == 0:
		print("Discriminant is strictly equal to zero, the solution is:", "\n{0:.6f}".format((-1 * (b / ( 2 * a)))))
		exit()
	if delta > 0:
		print("Discriminant is strictly positive, the two solutions are:")
		print("{0:.6f}".format(((b * -1) - (delta ** 0.5)) / (2 * a)))
		print("{0:.6f}".format(((b * -1) + (delta ** 0.5)) / (2 * a)))
		exit()



def printSolution(l):
	deg = printDegree(l)
	if deg > 2:
		print("The polynomial degree is strictly greater than 2, I can't solve.")
		exit()
	if deg == 0:
		print("The solution is:\n0")
		exit()
	if deg == 1:
		print("The solution is:")
		print(resolveFirst(l))
		exit()
	if (deg == 2):
		resolveSecond(l)
		exit()

def main():
	if len(sys.argv) != 2:
		print("Error\nUsage: python3 computerv1.py <equation to solve>", file=sys.stderr)
		exit()
	ex  = sys.argv[1]
	l = parseArg(ex)
	if (len(l) % 2 or len(l) == 0):
		print("Error\nInvalid Equation")
		exit()
	l = simplifyList(l)
	printReduced(l)
	printSolution(l)

if __name__ == "__main__":
	main()