import Lexis
allDefinitions = ""

def termgen(rule,sym,node,str):
    global allDefinitions
    allDefinitions +=  "        %s/k -> $m=self.mark()$ '%s' $k=%s('%s',m.start)$ ;\n" %  (rule,sym,node,str)

def kwgen(rule,sym=None,str=None):
    if not sym:
        sym = rule
        str = rule
    termgen("kw%s"%rule,sym,"KeyWordNode",str)

def kwsgen(kws):
    for kw in kws:
        kwgen(kw)


def opgen(rule,sym,str):
    termgen("op%s"%rule,sym,"OpNode",str)

def tokgen(rule,sym,str):
    termgen("tok%s"%rule,sym,"TokNode",str)
        
def sepgen(rule,sym,str):
    termgen("tok%s"%rule,sym,"SepNode",str)

def generateAll():
    kwsgen(Lexis.keywords)

    kwgen('AtoB','\-\>','->')
    kwgen('PortToPort','\<\=\>','<=>')    
#    kwgen('AwithB','\<\-\>','<->')
    kwgen('ARROW','\=\>','=>')

    opgen("EQ","\=","=")
    opgen('SUP', '\<\:', '<:')
    opgen('HASH', '\#', '#')
    opgen('LTEQ', '\<\=', '<=')
    opgen('GTEQ', '\>\=', '>=')
    opgen('LT', '\<', '<')
    opgen('GT', '\>', '>')
    opgen('IN', 'IN', 'IN')
    opgen('PLUS', '\+', '+')
    opgen('AGGR', '\@', '@')
    opgen('MINUS', '\-', '-')
    opgen('AMP', '\&', '&')
    opgen('TIMES', '\*', '*')
    opgen('DIVIDE', '\/', '/')
    opgen('DIV', 'DIV', 'DIV')
    opgen('MOD', 'MOD', 'MOD')
    opgen('AND', 'AND', 'AND')
    opgen('NOT', 'NOT', 'NOT')
    opgen('OR', 'OR', 'OR')
    opgen('CARET', '\^', '^')

    tokgen('LCR','\{','{')
    tokgen('RCR','\}','}')
    tokgen('LBR','\(','(')
    tokgen('RBR','\)',')')
    tokgen('LSQ','\[','[')
    tokgen('RSQ','\]',']')
    tokgen('ASS','\:\=',':=')
    tokgen('COL','\:',':') 
    tokgen('TILDE', '\~', '~')


    sepgen('SEMI','\;',';')
    sepgen('COMMA','\,',',')
    sepgen('PIPE','\|','|')
    sepgen('DOTDOT','\.\.','..')
    sepgen('DOT','\.','.')

    return allDefinitions

if __name__ == "__main__":
    print generateAll() #OK
