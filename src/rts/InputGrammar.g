	separator comment:         '\%.*' ;
	separator continueComment: '\\[ \r\f\v\t]*\%[^\n]*\n' ;
	separator continue:        '\\[ \r\f\v\t]*\n' ;
	separator white:           '[ \r\f\v\t]' ;
    token wild:                '\*' ;
    token opIN:                '\>' ;
    token opOUT:               '\<' ;

    token opQUE:               '\?' ;
    token opCOL:               '\:' ;
    token opDOTDOT:            '\.\.' ;
    token opDOT:               '\.' ;

    token opDSBR:              '\]\]' ;     
    token opDSBL:              '\[\[' ;     

    token opSBR:               '\]' ;     
    token opSBL:               '\[' ;     

    token opCBR:               '\}' ;     
    token opCBL:               '\{' ;     

    token opBANG:              '\!' ;
 
    token opCOM:               '\,' ;

    token opTEST:              '==' ;

    token opEQ:                '\=' ;

	token floatval:            '\d+\.\d+' float ;
	token intval:              '\d+' int ;
	token stringval:           "\"(\\.|[^\"\\]+)*\"|'(\\.|[^'\\]+)*'" stripQuotes ;
	token symbol:              '\w+' ;
	token sep:                 '\n' ;
 

	START/l ->  cmds/l;


#	cmds/cs -> cmd/c seps cmds/cs $ cs = [c] + cs $ # Note the prepend
#		    |  cmd/c seps $ cs = [c] $
#		    |  cmd/c $ cs = [c] $
#		    |  seps cmds/cs
#            |  seps $ cs = None $;

    cmds/cs ->  seps? $ cs=[] $ (cmdsep/c $ cs.append(c) $)*
            |   seps $ cs = None $;

    cmdsep/c -> cmd/c seps? ;

    cmd/c   -> inpcmd/c
            |  announcecmd/c
            |  elapsecmd/c 
            |  elapsedcmd/c
            |  expectcmd/c
            |  testvalcmd/c;


    inpcmd/c -> opIN  (symbol/port opDOT | $ port='' $) symbol/msg params/l 
        $ c = Command.ScriptMsgCommand (portName=port, msgName=msg, inpLine=l, lastLine=self.line()) $ ;
           
    elapsecmd/c -> opQUE intval/q symbol/f 
        $ c = Command.ElapseCommand(quantity=q, factor=f, lastLine=self.line()) $ ;

    announcecmd/c -> opCOL symbol/x nestedref/s value/v 
        $ c = Command.DataportSetCommand(portName=s, value=v, lastLine=self.line()) $ ;

    elapsedcmd/c -> opBANG scaleList/l
        $ c = Command.ElapsedCommand(absTime=l, lastLine=self.line()) $;

    expectcmd/c -> opOUT (opSBL timeConstraint/tc1 opCOM timeConstraint/tc2 opSBR| $ tc1=None; tc2=None $ )  
                         (symbol/port opDOT | $ port='' $) 
                         symbol/msg params/l
        $ c = Command.ExpectCommand(earliest=tc1, latest=tc2, portName=port, msgName=msg, params=l, lastLine=self.line()) $;

    testvalcmd/c -> opTEST nestedref/nr ( value/v | $v=None$ )  
        $ c = Command.TestValueCommand(name=nr, value=v, lastLine=self.line()) $;

    timeConstraint/t -> wild/t | scaleList/t ;

    nestedref/l -> symbol/s $ l = [s] $ (opDOT symbol/s $ l.append(s) $ )* ;

    params/l   -> $ l = [] $ ( elt/e $ l.append(e) $ (opCOM elt/e $ l.append(e) $)* )? ;

    lst/l -> $ l = [] $  (value/v (opCOM)?  $ l.append(v) $ )* ;
    dct/d -> $ d = {} $  (value/s opCOL value/v  $ d[str(s)] = v $ (opCOM)? )* ;
    elt/e   -> symbol/s opEQ value/v $ e = s,v $ ;

    sign/s  -> '-' $ s = -1 $ ;

    value/v -> wild $ v = Command.Any() $
            |  symbol/v
	        |  stringval/v
            |  scaleList/v
            |  number/v 
            |  opDSBL choices/v  opDSBR
            |  opSBL lst/v opSBR 
            |  opCBL dct/v opCBR ;

    choices/a -> value/v1 opDOTDOT value/v2 $ a =Command.Range(v1,v2) $
              |  value/v $ l = [v] $ (';' value/v $ l.append(v) $)* $ a= Command.Alternatives(l) $;

    scaleList/l -> number/n symbol/s $ l=[(n,s)] $ ( '\+' number/n symbol/s $ l.append((n,s)) $ )* ;

    number/n -> $ s=1
                (sign/s)? (floatval/v|intval/v) $ n = v * s $ ;
 
    seps    -> sep seps
            |  sep ;
	
