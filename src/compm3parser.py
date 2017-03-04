import generateTerminals

style = "new"

if style == "old":
    import tpg
    src = tpg.translate(open("m3.g").read())
    srcfile = open("m3parser.py","w")
    srcfile.write(src)
    srcfile.close()
elif style == "new":
    grammar = open("m3.g", "r").read()
    m3parser = open("m3parser.py", "w")
    m3parser.write("""
import tpg
from Nodes import *
from RuleNodes import *
class Parser(tpg.Parser):
""")
    m3parser.write('    r"""\n')
    m3parser.write(grammar)
    m3parser.write(generateTerminals.generateAll())
    m3parser.write('\n"""\n')
    #pygOut.write('    verbose = 2\n')
    m3parser.close()

else:
    raise "Silly Tool Problem"

