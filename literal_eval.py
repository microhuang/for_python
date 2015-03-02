# study_for_python

import ast

ast.literal_eval('1+2')

#ast.literal_eval('__import__("os").system("dir")') #安全
eval('__import__("os").system("dir")')              #不安全
