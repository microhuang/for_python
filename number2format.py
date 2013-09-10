import string

def format(number, radix, digits=string.digits+string.ascii_lowercase):
	if not 2 <= radix <= len(digits):
		raise ValueError, "radix must be in 2..%r, not %r" % (len(digits), radix)
	result=[]
	addon=result.append
	sign=''
	if number<0:
		number=-number
		sign='-'
	elif number==0:
		sign='0'
	_divmod=divmod
	while number:
		number, rdigit = _divmod(number, radix)
		addon(digits[rdigit])
	addon(sign)
	result.reverse()
	return ''.join(result)


as_str='abc'
as_num=13368L
num=int(as_str,36)
assert num == as_num
res=format(num,36)
assert res == as_str
