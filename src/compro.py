#
# Pre-cookers for the lexer
#

# kill nested comments
def commentkiller(prgstr):
    depth = 0
    resstr = ""
    for idx in range(len(prgstr)-1):
        nxtpair = prgstr[idx:idx+2]
        if nxtpair == "(*":
            depth += 1
        if nxtpair == "*)":
            if depth > 1:
                prgstr = prgstr[:idx] + "." + prgstr[idx+1:]
            depth -= 1
    
    return prgstr
        
# kill funny German characters



def umlautkiller(prgstr):
    ttable = {'\xe4': "ae", '\xf6': "oe", '\xfc': "ue", '\xc4': "Ae", '\xd6': "Oe", '\xdc': "Ue", '\xdf': "ss"}
    def transform(ch):
        # TBD FIX ME !!! (this currently isn't catching anything)
        if ch in ttable:
            return ttable[ch] 
        else:
            return "?"
    for idx in range(len(prgstr)):
        if ord(prgstr[idx]) > 128:
            prgstr = prgstr[:idx] + transform(prgstr[idx]) + prgstr[idx+1:]
    return prgstr


