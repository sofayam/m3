import os
import Options
# generate bits of the manual from the program text

docbase = os.environ["M3_HOME"] + os.sep + "doc" + os.sep
doc = None

def startDoc(name):
    global doc
    if Options.options.genDoc:
        doc = open(docbase + name, "w")
def addGroup(header):
    if Options.options.genDoc:
        doc.write(header + "\n" + "\\begin{itemize}\n")
def addItem(name, expl):
    if Options.options.genDoc:
        doc.write("\item %s : %s\n" % (name,expl))
def endGroup():
    if Options.options.genDoc:
        doc.write("\\end{itemize}\n")
def endDoc():
    if Options.options.genDoc:
        doc.close()
