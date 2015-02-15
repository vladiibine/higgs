import ast

expr = """\
class Asdf(object):
    def meme(self, x):
        return 15

a = Asdf()

x = a.meme(a)
if x:
    print x
"""


a1 = ast.parse(expr)

0