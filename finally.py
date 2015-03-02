def FinallyTest():
	print('i am starting...')
	while True:
		try:
			print('i am running...')
			raise IndexError("r")
		except(NameError):
			print('NameError happended')
			break
		#except(IndexError):
		#	print('IndexError')
		#	break
		#except:
		#	print('except')
		#	break
		finally:
			print('finally executed')
			break                                      #finally中的break、return等语句可能导致未被捕获的IndexError错误丢失--未能先函数外传递
			
FinallyTest()
