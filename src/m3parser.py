
import tpg
from Nodes import *
from RuleNodes import *
class Parser(tpg.Parser):
    r"""
        set lexer = Lexer
        set lexer_dotall = True
        token TextLiteralTok:     "\"(\\.|[^\"\\]+)*\"" ; 
        token CharLiteralTok:     "'(\\.|[^'\\]+)*'" ; 

        separator comment:     '\(\*.*?\*\)' ;
        separator white:       '[ \r\f\v\t\n]' ;
        separator pragma:      '\<\*.*?\*\>' ;
        token LBR:             '\(' ; # TBD these are left up here to work around lex priority problem with comments
        token RBR:             '\)' ;
          
        token IntTok:          '\d+' ; 
        token IdTok:           '[A-Za-z]\w*' ;


        START/c       -> Compilation/c ;

        Compilation/c -> (kwUNSAFE)? (CapsuleInterface/c | Capsule/c | Interface/c | Module/c | GenInf/c | GenMod/c) ; 
        # TBD Nothing is unsafe


        CapsuleInterface/ci                                                          #RTMX -
                      -> kwCAPSULE/kwc kwINTERFACE/kwi Id/n tokSEMI/ts 
                         $ii=ImportListNode()$ (Import/i $ii.add(i)$)* 
                         PortList/pl kwEND/kwe Id/endId tokDOT/td
                         $ci=CapsuleInterfaceNode(NullNode(),kwc,kwi,n,ts,ii,pl,kwe,endId,td)$ ;

        Capsule/c     -> kwCAPSULE/kwc Id/n                  #RTMX -
                         (kwIMPLEMENTS/kwi Id/implId|$kwi=NullNode(); implId=NullNode()$)
                         tokSEMI/ts                                     
                         $ii=ImportListNode()$ (Import/i $ii.add(i)$)* 
                         $ucl=UseCapsuleListNode()$ (UseCapsule/uc $ucl.add(uc)$)*
                         CapsuleBlock/cb
                         Id/endId tokDOT/td
                         $c=CapsuleNode(NullNode(),kwc,n,kwi,implId,ts,ii,ucl,cb,endId,td)$ ;
             

        Interface/i   -> kwINTERFACE/kwi Id/n tokSEMI/ts 
                         $ii=ImportListNode()$ (Import/i $ii.add(i)$)* 
                         $dl=InterfaceDeclListNode()$ (Decl/d $dl.add(d)$)* kwEND/kwe Id/endId tokDOT/td
                         $i=InterfaceNode(NullNode(),kwi,n,ts,ii,dl,kwe,endId,td)$
                      |  kwINTERFACE/kwi Id/n opEQ/kweq Id/gn GenActls/ga kwEND/kwe Id/endId tokDOT/td 
                         $i=InterfaceInstantiationNode(NullNode(),kwi,n,kweq,gn,ga,kwe,endId,td)$ ;

        Module/m      -> kwMODULE/kwm Id/n $ii=ImportListNode()$ 
                         (kwEXPORTS/kwex IdList/ei|$kwex=NullNode(); ei=NullNode()$)? tokSEMI/ts 
                         (Import/i $ii.add(i)$)* Block/b Id/endId tokDOT/td 
                         $m=ModuleNode(NullNode(),kwm,n,kwex,ei,ts,ii,b,endId,td)$
                      |  kwMODULE/kwm Id/n  (kwEXPORTS/kwex IdList/ei|$ei=NullNode(); kwex=NullNode()$)? 
                         opEQ/kweq Id/gn GenActls/ga kwEND/kwe Id/endId tokDOT/td 
                         $m=ModuleInstantiationNode(NullNode(),kwm,n,kwex,ei,kweq,gn,ga,kwe,endId,td)$ ;

        GenInf/g      -> kwGENERIC/kwg kwINTERFACE/kwi Id/id GenFmls/gf tokSEMI/ts $il=ImportListNode()$ (Import/i $il.add(i)$)* 
                         $dl=InterfaceDeclListNode()$ (Decl/d $dl.add(d)$)* kwEND/kwe Id/endId tokDOT/td 
                         $g=GenericInterfaceNode(NullNode(),kwg,kwi,id,gf,ts,il,dl,kwe,endId,td)$ ;
        GenMod/g      -> kwGENERIC/kwg kwMODULE/kwm Id/i GenFmls/gf tokSEMI/ts 
                         $il=ImportListNode()$ (Import/imp $il.add(imp)$)* 
                         Block/b Id/endId tokDOT/td $g=GenericModuleNode(NullNode(),kwg,kwm,i,gf,ts,il,b,endId,td)$ ;      

        UseCapsule/uc    -> kwUSECAPSULE/kwu IdList/il tokSEMI/ts $uc=UseCapsuleNode(kwu,il,ts)$ ; #RTMX -
        Import/i         -> AsImport/i | FromImport/i ;
        AsImport/ai      -> $ail=AsImportListNode()$ kwIMPORT/kwi ImportItem/i $ail.add(i)$ 
                            (tokCOMMA/tc $ail.add(tc)$ ImportItem/i $ail.add(i)$)* tokSEMI/ts $ai=AsImportNode(kwi,ail,ts)$;
        FromImport/fi    -> kwFROM/kwf Id/i kwIMPORT/kwi IdList/il tokSEMI/ts $fi=FromImportNode(kwf,i,kwi,il,ts)$ ;

        Block/b          -> $dl=DeclListNode()$ (Decl/d $dl.add(d)$)* kwBEGIN/kwb S/s kwEND/kwe $b=BlockNode(dl,kwb,s,kwe)$ ;
        CapsuleBlock/b   -> $dl=DeclListNode()$ (Decl/d $dl.add(d)$)* $c=NullNode()$ (Connections/c)? kwBEGIN/kwb S/s kwEND/kwe 
                            $b=CapsuleBlockNode(dl,c,kwb,s,kwe)$ ;

        AnyConnection/c   -> Connection/c | PortConnection/c;
        Connection/cs     -> QualId/end1 kwAtoB/c QualId/end2 $cs=ConnectionNode(end1,c,end2)$;
        PortConnection/cs -> QualId/end1 kwPortToPort/c QualId/end2 $cs=PortConnectionNode(end1,c,end2)$;
        Connections/cs    -> kwCONNECT/kwc $cl=ConnectionListNode()$ AnyConnection/c $cl.add(c)$ (tokSEMI/ts AnyConnection/c $cl.add(ts); cl.add(c)$)* 
                            (tokSEMI/ts|$ts=NullNode()$)? 
                            $cs=ConnectionsNode(kwc,cl,ts)$ ;

        Decl/d        -> kwCONST/kwc  $cl=ConstDeclsListNode()$ (ConstDecl/c $cl.add(c)$ tokSEMI/ts $cl.add(ts)$)* $d=ConstDeclsNode(kwc,cl)$ 
                      |  kwTYPE/kwt  $tl=TypeDeclsListNode()$ (TypeDecl/t $tl.add(t)$ tokSEMI/ts $tl.add(ts)$)* $d=TypeDeclsNode(kwt,tl)$ 
                      |  kwEXCEPTION/kwe  $el=ExceptionDeclsListNode()$ (ExceptionDecl/e $el.add(e)$ tokSEMI/ts $el.add(ts)$)* 
                         $d=ExceptionDeclsNode(kwe,el)$ 
                      |  kwVAR/kwv $vl=VariableDeclsListNode()$ (VariableDecl/v $vl.add(v)$ tokSEMI/ts $vl.add(ts)$)*
                         $d=VariableDeclsNode(kwv,vl)$ 
                      |  ProcedureHead/p (opEQ/kweq Block/b (Id/endId|$endId=NullNode()$) | $kweq=NullNode(); b=NullNode(); endId=NullNode()$)? tokSEMI/ts 
                         $d=ProcedureDeclNode(p,kweq,b,endId,ts)$ 
                      |  ActivityHead/h opEQ/kweq Block/b (Id/endId|$endId=NullNode()$)
                         AfterClause/ac tokSEMI/ts                  # RTMX
                         $d=ActivityDeclNode(h,kweq,b,endId,ac,ts)$ 
                      |  kwTRIGGER/kwt Id/triggerId kwON/kwo Expr/e tokSEMI/ts 
                         $d=TriggerNode(kwt,triggerId,kwo,e,ts)$                                              # RTMX
                      |  kwSTATE/kws Id/stateId $tl=TransitionListNode()$                                     # RTMX
                         (TransitionDecl/t $tl.add(t)$ (tokSEMI/ts TransitionDecl/t $tl.add(ts); tl.add(t)$)* )? tokSEMI/ts 
                         $d=StateDeclNode(kws,stateId,tl,ts)$ 
                      |  kwSTART/kws opEQ/kweq kwBEGIN/kwb S/s kwEND/kwe tokSEMI/ts $d=StartDeclNode(kws,kweq,kwb,s,kwe,ts)$ # RTMX
                      |  kwREVEAL/kwr $l=RevealsListNode()$ (Reveal/r $l.add(r)$)* $d=RevealsNode(kwr,l)$   
                      |  (kwREADS/kwd|kwWRITES/kwd) QualId/q tokSEMI/ts 
                            $d=DataDependencyNode(kwd,q,ts)$                        # RTMX (used only in activities and transitions)
                      |  kwSENDS/kws QualId/q tokSEMI/ts
                            $d=SendsDeclNode(kws,q,ts)$ ;                      # RTMX (used only in activities and transitions)
            

        TransitionDecl/t  -> TransitionHead/th opEQ/kweq Block/b (Id/endId|$endId=NullNode()$) 
                             AfterClause/ac
                             $t=TransitionDeclNode(th,kweq,b,endId,ac)$ ;
        TransitionHead/th -> kwON/kwo Id/name MsgSignature/sig $th=TransitionHeadNode(kwo,name,sig)$ ;


        Reveal/r      -> QualId/q  (opEQ/o | opSUP/o)  Type/t  tokSEMI/ts $r=RevealNode(q,o,t,ts)$ ;

        GenFmls/gf    -> tokLBR/lbr (IdList/il|$il=NullNode()$)? tokRBR/rbr $gf=GenFormalsNode(lbr,il,rbr)$ ; 
        GenActls/ga   -> tokLBR/lbr (IdList/il|$il=NullNode()$)? tokRBR/rbr $ga=GenActualsNode(lbr,il,rbr)$ ; 

        ImportItem/ii -> Id/oi kwAS/kwa Id/ni $ii=RenamedImportItemNode(oi,kwa,ni)$
                      |  Id/i $ii=ImportItemNode(i)$ ;

        ConstDecl/cd      -> Id/i  (tokCOL/col Type/t|$col=NullNode(); t=NullNode()$)? 
                                  opEQ/kweq ConstExpr/ce  $cd=ConstDeclNode(i,col,t,kweq,ce)$ ;
        
        TypeDecl/td       -> Id/i (opEQ/s | opSUP/s)  Type/t $td=TypeDeclNode(i,s,t)$ ;

        ScaledType/s      -> kwSCALED/kws TypeName/tn tokLCR/lcr Id/unit $scaleList=ScaleListNode()$ 
                                (ScaleElt/se $scaleList.add(se)$)* tokRCR/rcr 
                                $s=ScaledTypeNode(kws, tn, lcr, unit, scaleList, rcr)$;

        ScaleElt/s       -> opTIMES/ttim Number/n opEQ/teq Id/i $s=ScaleEltNode(ttim, n, teq, i)$;

        ExceptionDecl/ed  -> Id/i (tokLBR/lbr Type/t tokRBR/rbr|$lbr=NullNode(); t=NullNode(); rbr=NullNode()$)? 
                               $ed=ExceptionDeclNode(i,lbr,t,rbr)$ ;
        VariableDecl/vd   -> IdList/il tokCOL/col Type/t tokASS/ass Expr/e $vd=VariableDeclNode(il,col,t,ass,e)$  
                          |  IdList/il tokCOL/col Type/t $vd=VariableDeclNode(il,col,t,NullNode(),NullNode())$
                          |  IdList/il tokASS/ass Expr/e $vd=VariableDeclNode(il,NullNode(),NullNode(),ass,e)$ ; 

        ProcedureHead/ph -> kwPROCEDURE/kwp Id/i Signature/s $ph=ProcedureHeadNode(kwp,i,s)$ ;

        ActivityHead/h -> kwACTIVITY/kwa Id/i MsgSignature/s $h=ActivityHeadNode(kwa,i,s)$ ;

        Signature/s      -> tokLBR/lbr Formals/f tokRBR/rbr  (tokCOL/col Type/t|$col=NullNode(); t=NullNode()$)? 
                            $r=NullNode(); kwr=NullNode()$ (kwRAISES/kwr Raises/r)? 
                            $s=SignatureNode(lbr,f,rbr,col,t,kwr,r)$ ;

        MsgSignature/s      -> tokLBR/lbr Formals/f tokRBR/rbr $col=NullNode(); t=NullNode(); r=NullNode(); kwr=NullNode()$     # RTMX
                            $s=SignatureNode(lbr,f,rbr,col,t,kwr,r)$ ;

        MethodSignature/s -> tokLBR/lbr Formals/f tokRBR/rbr  (tokCOL/col Type/t|$col=NullNode(); t=NullNode()$)? $r=NullNode(); kwr=NullNode()$ 
                            (kwRAISES/kwr Raises/r)? 
                            $s=MethodSignatureNode(lbr,f,rbr,col,t,kwr,r)$ ;

        Formals/fs       -> $fs=FormalsNode()$ ( Formal/f $fs.add(f)$ ( tokSEMI/ts Formal/f $fs.add(ts); fs.add(f)$)* (tokSEMI/ts $fs.add(ts)$)? )? ;

        Formal/f         -> $m=NullNode()$ (Mode/m)? IdList/il tokCOL/col Type/t tokASS/ass ConstExpr/ce $f=FormalNode(m,il,col,t,ass,ce)$
                         |  $m=NullNode()$ (Mode/m)? IdList/il tokCOL/col Type/t $f=FormalNode(m,il,col,t,NullNode(),NullNode())$ 
                         |  $m=NullNode()$ (Mode/m)? IdList/il tokASS/ass ConstExpr/ce $f=FormalNode(m,il,NullNode(),NullNode(),ass,ce)$  ;

        Mode/kwm        -> kwVALUE/kwm | kwVAR/kwm | kwREADONLY/kwm ;
        Raises/r        -> $rl=RaisesListNode()$ tokLCR/lcr ( QualId/qi $rl.add(qi)$ ( tokCOMMA/tc $rl.add(tc)$ QualId/qi $rl.add(qi)$ )* )? 
                           tokRCR/rcr $r=RaisesNode(lcr,rl,rcr)$ 
                        |  kwANY/kwa $r=RaisesAnyNode(kwa)$ ;

        Stmt/s        -> NextSt/s | AssignSt/s | CallSt/s 
                      |  Block/s |  CaseSt/s | ExitSt/s | EvalSt/s | ForSt/s | ForEachSt/s 
                      |  IfSt/s | LockSt/s | LoopSt/s | RaiseSt/s | RepeatSt/s | ReturnSt/s
                      |  TCaseSt/s | TryXptSt/s | TryFinSt/s | WhileSt/s | WithSt/s 
                      |  SendSt/s | PythonSt/s  | ResetSt/s | SynCallSt/s | AssertSt/s | ReplySt/s ;

        S/ss          -> $ss=StatementsNode()$ (Stmt/s $ss.add(s)$ (tokSEMI/ts1 Stmt/s $ss.add(ts1); ss.add(s)$)* (tokSEMI/ts2 $ss.add(ts2)$)? )? ;

        AssignSt/as   -> Expr/lhs tokASS/ass Expr/rhs $as=AssignStNode(lhs,ass,rhs)$ ;
        NextSt/ns     -> kwNEXT/kwn Id/stateId $ns=NextStNode(kwn,stateId)$ ;

        AfterClause/ac -> ( kwAFTER/kwa Expr/ae | $kwa=NullNode(); ae=NullNode()$) $ac=AfterClauseNode(kwa,ae)$ ;

        SendSt/ss     -> kwSEND/kws Expr/e AfterClause/ac $ss=SendStNode(kws,e,ac)$ ;
        SynCallSt/ss  -> kwCALL/kwc Expr/e $ss=SynCallStNode(kwc,e)$ ;
        ReplySt/ss    -> kwREPLY/kwr Expr/e AfterClause/ac $ss=ReplyStNode(kwr,e,ac)$ ;
        AssertSt/as   -> kwASSERT/kwa Expr/e $as=AssertStNode(kwa,e)$;
        PythonSt/ps   -> kwPYTHON/kwp TextLiteral/l $ps=PythonStNode(kwp,l)$ ;
        ResetSt/ps    -> kwRESET/kwr ( Expr/level | $level=NullNode()$ ) $ps=ResetStNode(kwr,level)$ ;

        CallSt/cs     -> Expr/e $cs=CallStNode(e)$; # We catch this later to check that it is really a call
        CaseSt/cs     -> $cl=CaseEltListNode()$ kwCASE/kwc Expr/ce kwOF/kwo (Case/c $cl.add(c)$)? 
                         (tokPIPE/tp $cl.add(tp)$ Case/c $cl.add(c)$)* 
                         (kwELSE/kwel S/s|$s=NullNode(); kwel=NullNode()$)? kwEND/kwe
                         $cs=CaseStNode(kwc,ce,kwo,cl,kwel,s,kwe)$ ;

        ExitSt/es     -> kwEXIT/kwe $es=ExitStNode(kwe)$ ;
        EvalSt/es     -> kwEVAL/kwe Expr/e $es=EvalStNode(kwe,e)$ ;
        ForSt/fs      -> kwFOR/kwf ForId/fi tokASS/ass Expr/se kwTO/kwt Expr/te 
                         (kwBY/kwb Expr/be|$kwb=NullNode(); be=NullNode()$)? 
                         kwDO/kwd S/s kwEND/kwe 
                         $fs=ForStNode(kwf,fi,ass,se,kwt,te,kwb,be,kwd,s,kwe)$ ;
        ForEachSt/fes -> kwFOREACH/kwf ForId/fi opIN/tin Expr/listExpr kwDO/kwd S/s kwEND/kwe
                         $fes=ForEachStNode(kwf,fi,tin,listExpr,kwd,s,kwe)$ ;                    # RTMX
        IfSt/ifs      -> kwIF/kwi Expr/ie kwTHEN/kwt S/ifc $eil=ElsifListNode()$ (Elsif/ei $eil.add(ei)$)* 
                         $es=NullNode(); kwel=NullNode()$ (kwELSE/kwel S/es)? kwEND/kwe 
                         $ifs=IfStNode(kwi,ie,kwt,ifc,eil,kwel,es,kwe)$ ;
        LockSt/ls     -> kwLOCK/kwl Expr/e kwDO/kwd S/s kwEND/kwe $ls=LockStNode(kwl,e,kwd,s,kwe)$ ;
        LoopSt/ls     -> kwLOOP/kwl S/s kwEND/kwe $ls=LoopStNode(kwl,s,kwe)$ ;
        RaiseSt/rs    -> kwRAISE/kwr QualId/ri $lbr=NullNode(); e=NullNode(); rbr=NullNode()$ (tokLBR/lbr Expr/e tokRBR/rbr)? 
                         $rs=RaiseStNode(kwr,ri,lbr,e,rbr)$ ;
        RepeatSt/rs   -> kwREPEAT/kwr S/s kwUNTIL/kwu Expr/e $rs=RepeatStNode(kwr,s,kwu,e)$ ;
        ReturnSt/rs   -> kwRETURN/kwr (Expr/e | $e=NullNode()$)? $rs=ReturnNode(kwr,e)$ ;

        TCaseSt/ts    -> kwTYPECASE/kwt Expr/e kwOF/kwo $tcl=TCaseListNode()$
                         (TCase/tc $tcl.add(tc)$)? (tokPIPE/tp $tcl.add(tp)$ TCase/tc $tcl.add(tc)$)* 
                         (kwELSE/kwel S/es|$es=NullNode(); kwel=NullNode()$)? kwEND/kwe 
                         $ts=TCaseStNode(kwt,e,kwo,tcl,kwel,es,kwe)$ ;
        TCase/t       -> $tl=TypeListNode()$ Type/t $tl.add(t)$ (tokCOMMA/tc $tl.add(tc)$ Type/t $tl.add(t)$)* 
                         (tokLBR/lbr TCaseId/i tokRBR/rbr |$i=NullNode(); lbr=NullNode(); rbr=NullNode()$)? kwARROW S/s 
                         $t=TCaseNode(tl,lbr,i,rbr,s)$ ;

        TryXptSt/ts   -> kwTRY/kwt S/s kwEXCEPT/kwex $hl=HandlerListNode()$ 
                         (Handler/h $hl.add(h)$)? (tokPIPE/tp $hl.add(tp)$ Handler/h $hl.add(h)$)* 
                         (kwELSE/kwel S/es|$es=NullNode(); kwel=NullNode()$)? kwEND/kwe $ts=TryXptStNode(kwt,s,kwex,hl,kwel,es)$ ;
        TryFinSt/tfs  -> kwTRY/kwt S/ts kwFINALLY/kwf S/fs kwEND/kwe $tfs=TryFinStNode(kwt,ts,kwf,fs,kwe)$ ;
        WhileSt/ws    -> kwWHILE/kww Expr/e kwDO/kwd S/s kwEND/kwe $ws=WhileStNode(kww,e,kwd,s,kwe)$ ;
        WithSt/ws     -> kwWITH/kww $bl=BindingListNode()$ Binding/b $bl.add(b)$ (tokCOMMA/tc $bl.add(tc)$ Binding/b $bl.add(b)$)* 
                         kwDO/kwd S/s kwEND/kwe $ws=WithStNode(kww,bl,kwd,s,kwe)$;

        Elsif/ei      -> kwELSIF/kwe Expr/e kwTHEN/kwt S/s $ei=ElsifNode(kwe,e,kwt,s)$ ;

        

        Case/c        -> LabelsList/ll kwARROW/kwa S/s $c=CaseNode(ll,kwa,s)$ ;
        VCase/c       -> LabelsList/ll kwARROW/kwa Fields/f $c=VCaseNode(ll,kwa,f)$ ;

        LabelsList/ll -> $ll=LabelsListNode()$ Labels/l $ll.add(l)$ (tokCOMMA/tc $ll.add(tc)$ Labels/l $ll.add(l)$)* ;

        Labels/ll     -> $ll=LabelsNode()$ ConstExpr/ce $ll.add(ce)$ (tokDOTDOT/tdd $ll.add(tdd)$ ConstExpr/ce $ll.add(ce)$)? ;

        Handler/h     -> $hl=HandlerQualidListNode()$ QualId/qi $hl.add(qi)$ (tokCOMMA/tc $hl.add(tc)$ QualId/qi $hl.add(qi)$)* 
                         (tokLBR/lbr Id/i tokRBR/rbr|$i=NullNode(); lbr=NullNode(); rbr=NullNode()$)? kwARROW/kwa S/s 
                         $h=HandlerNode(hl,lbr,i,rbr,kwa,s)$ ; 
        Binding/b     -> Id/i opEQ/kweq Expr/e $b=BindingNode(i,kweq,e)$;
        Actual/a      -> (Id/i tokASS/ass |$i=NullNode(); ass=NullNode()$)? Expr/e $a=ActualExprNode(i,ass,e)$
                      |  Type/t $a=ActualNode(t)$ ; # swapped these round (used by narrow e.g, maybe by generics)

        Type/t        -> TypeSingle/t1 opAGGR/o Type/t2 $t=AggregatedProtocolNode(t1,o,t2) 
                      |  TypeSingle/t ;

        TypeSingle/t  -> ObjectType/t 
                      |  TypeName/t | ArrayType/t 
                      |  PackedType/t | EnumType/t 
                      |  ProcedureType/t | VariantRecordType/t | RecordType/t | RefType/t | SetType/t | SubrangeType/t
                      |  TimerType/t
                      |  ListType/t
                      |  DictType/t
                      |  ProtocolType/t
                      |  (tokLBR/lbr Type/t tokRBR/rbr $t=BracketedTypeNode(lbr,t,rbr)$) 
                      |  tokTILDE/tokt TypeSingle/pro $t=ConjugatedProtocolNode(tokt, pro)$
                      |  ScaledType/t;

                      

        ListType/t    -> kwLIST/kwl kwOF/kwo Type/t $t=ListNode(kwl,kwo,t)$ ;                         #RTMX
        DictType/t    -> kwDICT/kwd (Type/idx|$idx=NullNode()$) kwOF/kwo Type/elt $t=DictNode(kwd,idx,kwo,elt)$ ;       #RTMX


        TimerType/t   -> $tp=NullNode(); tv=NullNode()$ (TimerPeriodicity/tp TimerVariability/tv)?    # RTMX
                         kwTIMER/kwt $kwd=NullNode(); e=NullNode()$
                         (kwDELAY/kwd Expr/e)? $t=TimerNode(tp,tv,kwt,kwd,e)$ ; 

        ProtocolType/t -> kwPROTOCOL/kwp  $mgl=MessageGroupListNode()$ (MessageGroup/mg $mgl.add(mg)$)* kwEND/kwe 
                          $t=ProtocolNode(kwp,mgl,kwe)$ ; # RTMX

        TimerPeriodicity/tm -> (kwONESHOT/tm | kwPERIODIC/tm) ;     # RTMX
        TimerVariability/tm -> (kwCHANGEABLE/tm | kwFIXED/tm) ;     # RTMX

        PortList/pl   -> $pl=PortListNode()$ (Port/p $pl.add(p)$ (tokSEMI/ts Port/p $pl.add(ts); pl.add(p)$)* 
                         (tokSEMI/ts $pl.add(ts)$)? )? ; # RTMX

#        Port/pl       -> kwPORT/kwp Id/id $mgl=MessageGroupListNode()$ (MessageGroup/mg $mgl.add(mg)$)* kwEND/kwe # RTMX
#                         $pl = PortNode(kwp,id,mgl,kwe)$ ;  

        Port/p        -> kwPORT/kwp Id/id tokCOL/col Type/protocol $p = PortNode(kwp,id,col,protocol)$ ;


        MessageGroup/mg 
                      -> (kwSYNCHRONOUS/kwsyn | $kwsyn=NullNode()$) (kwINCOMING/kwdir | kwOUTGOING/kwdir) 
                         $ml=MessageListNode()$ Message/m $ml.add(m)$ (tokSEMI/ts Message/m $ml.add(ts);ml.add(m)$)* (tokSEMI/ts $ml.add(ts)$)? 
                         $mg=MessageGroupNode(kwsyn,kwdir,ml)$ ;
        Message/m     -> kwMESSAGE/kwm Id/id MsgSignature/s $m=MessageNode(kwm,id,s)$ ;

        ArrayType/a   -> kwARRAY/kwa $tl=TypeListNode()$ (Type/t $tl.add(t)$ (tokCOMMA/tc $tl.add(tc)$ Type/t $tl.add(t)$)*)? kwOF/kwo Type/t 
                         $a=ArrayNode(kwa,tl,kwo,t)$ ;
        PackedType/p  -> kwBITS/kwb ConstExpr/ce kwFOR/kwf Type/t $p=PackedNode(kwb,ce,kwf,t)$ ;
        EnumType/e    -> tokLCR/lcr  (IdList/i|$i=NullNode()$)? tokRCR/rcr $e=EnumNode(lcr,i,rcr)$ ;

        ObjectType/o  -> (TypeName/tn|$tn=NullNode()$)? (Brand/b|$b=NullNode()$)? kwOBJECT/kwob Fields/f 
                         (kwMETHODS/kwm Methods/m|$kwm=NullNode(); m=NullNode()$)? 
                         (kwOVERRIDES/kwov Overrides/o|$kwov=NullNode(); o=NullNode()$)? kwEND/kwe 
                         $ol=ObjectListNode()$ (ObjectType/o $ol.add(o)$)* 
                         $o=ObjectNode(tn,b,kwob,f,kwm,m,kwov,o,kwe,ol)$ ; # solve left recursion
        ProcedureType/p -> kwPROCEDURE/kwp Signature/s $p=ProcedureNode(kwp,s)$ ;
        VariantRecordType/v 
                        -> kwRECORD/kwr 

                         $cl=VCaseEltListNode()$ kwCASE/kwc Field/tagField kwOF/kwo (VCase/c $cl.add(c)$)? 
                         (tokPIPE/tp $cl.add(tp)$ VCase/c $cl.add(c)$)* 
                         (kwELSE/kwel Fields/efields |$efields=NullNode(); kwel=NullNode()$)? 
                         kwEND/kwce 
                         (tokSEMI/ts | $ts=NullNode()$)?
                         (Fields/sfields | $sfields=NullNode()$)?
                         kwEND/kwe
                         $v=VariantRecordNode(kwr,kwc,tagField,kwo,cl,kwel,efields,kwce,ts,sfields,kwe)$ ;

        RecordType/r    -> kwRECORD/kwr Fields/f kwEND/kwe $r=RecordNode(kwr,f,kwe)$ ;
        RefType/r       -> (kwUNTRACED/kwu|$kwu=NullNode()$)? (Brand/b|$b=NullNode()$)? kwREF/kwr Type/t $r=RefNode(kwu,b,kwr,t)$ ;
        SetType/s       -> kwSET/kws kwOF/kwo Constructor/sc $s=SetNode(kws,kwo,sc)$ ;
        SubrangeType/s  -> tokLSQ/lsq ConstExpr/ce1 tokDOTDOT/tdd ConstExpr/ce2 tokRSQ/rsq $s=SubrangeNode(lsq,ce1,tdd,ce2,rsq)$ ;
        Brand/b       -> kwBRANDED/kwb (TextLiteral/n|QualId/n|$n=NullNode()$)? $b=BrandNode(kwb,n)$; 
                         # restricted from ConstExpr
        Fields/fl     -> $fl=FieldListNode()$ ( Field/f $fl.add(f)$ (tokSEMI/ts Field/f $fl.add(ts); fl.add(f)$)* (tokSEMI/ts $fl.add(ts)$)? )? ;
        Field/f       -> 
                      (  IdList/i tokCOL/col Type/t tokASS/ass ConstExpr/ce
                      |  IdList/i tokCOL/col Type/t $ass=NullNode(); ce=NullNode()$
                      |  IdList/i tokASS/ass ConstExpr/ce $col=NullNode(); t=NullNode()$
                      )                   
                      $f=FieldNode(i,col,t,ass,ce)$ ;
        Methods/ml    -> $ml=MethodListNode()$ ( Method/m $ml.add(m)$ (tokSEMI/ts $ml.add(ts)$ Method/m $ml.add(m)$)* (tokSEMI/ts $ml.add(ts)$)? )? ;

        Method/m      -> Id/i MethodSignature/s (tokASS/ass ConstExpr/ce|$ass=NullNode(); ce=NullNode()$)? $m=MethodNode(i,s,ass,ce)$ ;
        Overrides/ol   -> $ol=OverrideListNode()$ ( Override/o $ol.add(o)$ (tokSEMI/ts Override/o $ol.add(ts); ol.add(o)$)* (tokSEMI/ts $ol.add(ts)$)? )? ;

        Override/o    -> Id/i tokASS/ass ConstExpr/ce $o=OverrideNode(i,ass,ce)$ ; 


        ConstExpr/ce  -> Expr/e $ce=ConstExprNode(e)$ ;

        Expr/ex       -> E0/e0 $ex=ExprNode(e0)$  ;

        E0/ex         -> $el=ExprListNode()$ E1/e1 (opOR/o  E1/e $el.add(OpExpNode(o,e))$)* 
                         $ex=BinaryExprNode(e1,el)$ ;
        E1/ex         -> $el=ExprListNode()$ E2/e1 (opAND/o  E2/e $el.add(OpExpNode(o,e))$)* 
                         $ex=BinaryExprNode(e1,el)$ ;
        E2/ex         -> $ol=OpListNode()$ (opNOT/o $ol.add(o)$)* E3/e $ex=UnaryExprNode(ol,e)$ ;
        E3/ex         -> $el=ExprListNode()$ E4/e1 (Relop/o E4/e $el.add(OpExpNode(o,e))$)* $ex=BinaryExprNode(e1,el)$ ;
        E4/ex         -> $el=ExprListNode()$ E5/e1 (Addop/o E5/e $el.add(OpExpNode(o,e))$)* $ex=BinaryExprNode(e1,el)$ ;
        E5/ex         -> $el=ExprListNode()$ E6/e1 (Mulop/o E6/e $el.add(OpExpNode(o,e))$)* $ex=BinaryExprNode(e1,el)$ ;
        E6/ex         -> $ol=OpListNode()$ (opPLUS/o $ol.add(o)$ | opMINUS/o  $ol.add(o)$)* 
                                          E7/e $ex=UnaryExprNode(ol,e)$ ;
        E7/ex         -> E8/e $sl=SelectorListNode()$ (Selector/s $sl.add(s)$)* 
                         $ex=SelectorExprNode(e,sl)$ ;
        E8/ex         -> Constructor/ex | tokLBR/lbr E0/e0 tokRBR/rbr $ex=BracketedExprNode(lbr,e0,rbr)$ 
                      | Number/ex | Id/ex | CharLiteral/ex | TextLiteral/ex ; #reordered

        Relop/o       ->  opEQ/o | opHASH/o | opLT/o  | opLTEQ/o | opGT/o | opGTEQ/o | opIN/o ;
        Addop/o       ->  opPLUS/o | opMINUS/o | opAMP/o ;
        Mulop/o       ->  opTIMES/o | opDIVIDE/o | opDIV/o | opMOD/o ;

        Selector/s    ->   opCARET/o $s=CaretNode(o)$ 
                      |    tokDOT/td Id/i $s=DotNode(td,i)$
                      |    $el=IndexListNode()$ tokLSQ/lsq E0/e $el.add(e)$ (tokCOMMA/tc $el.add(tc)$ E0/e $el.add(e)$)* tokRSQ/rsq 
                           $s=ArrayRefSelectorNode(lsq,el,rsq)$
                      |    $al=ActualListNode()$ tokLBR/lbr ( Actual/a $al.add(a)$ (tokCOMMA/tc $al.add(tc)$ Actual/a $al.add(a)$)* )? tokRBR/rbr 
                           $s=ProcCallSelectorNode(lbr,al,rbr)$ ; 

        Constructor/c  -> TypeSingle/t $lcr=NullNode(); cel=NullNode(); rcr=NullNode()$
                          (tokLCR/lcr $cel=ConsEltListNode()$
                           (ConsElt/ce $cel.add(ce)$
                            (tokCOMMA/tc $cel.add(tc)$ ConsElt/ce $cel.add(ce)$)*)? tokRCR/rcr)?
                          $c=ConstructorNode(t,lcr,cel,rcr)$ ;

        ConsElt/ce ->  Id/i tokASS/ass Expr/e $ce=ConsEltAssNode(i,ass,e)$
                   |   TextLiteral/t tokASS/ass Expr/e $ce=ConsEltDictNode(t,ass,e)$
                   |   Expr/e1 tokDOTDOT/tdd Expr/e2 $ce=ConsEltRangeNode(e1,tdd,e2)$
                   |   Expr/e $ce=ConsEltExprNode(e)$
                   |   tokDOTDOT/tdd $ce=ConsEltDotdotNode(tdd)$ ;


        IdList/il       -> $il=IdListNode()$ Id/i $il.add(i)$ (tokCOMMA/tc $il.add(tc)$ Id/i $il.add(i)$)* ;

        QualId/qi       -> $qi=QualIdNode()$ Id/i $qi.add(i)$ (tokDOT/td $qi.add(td)$ Id/i $qi.add(i)$)+  # I now swallow dot selects too
                        |  Id/i $qi=QualIdNode(); qi.add(i)$ ;

        TypeName/tn   -> QualId/qi $tn=TypeNameNode(qi)$
                      |  kwROOT/kwr $tn=RootNode(kwr)$
                      |  kwUNTRACED/kwu kwROOT/kwr $tn=UntracedRootNode(kwu,kwr)$ ;

        Number/n      -> Int/i $nr=NullNode(); td=NullNode(); scaling=NullNode()$ (tokDOT/td (Id/nr|Int/nr)?)? (Id/scaling)?
                         $n=NumberNode(i,td,nr,scaling)$ ; # TBD this needs to include bases etc.
  
        CharLiteral/l -> $m=self.mark()$ CharLiteralTok/t $l=CharLiteralNode(t,m.start)$ ;
        TextLiteral/l -> $m=self.mark()$ TextLiteralTok/t $l=TextLiteralNode(t,m.start)$ ;

        Id/i          -> $m=self.mark()$ IdTok/idt $i=IdNode(idt,m.start)$ ;
        ForId/i       -> $m=self.mark()$ IdTok/idt $i=ForIdNode(idt,m.start)$ ;
        TCaseId/i     -> $m=self.mark()$ IdTok/idt $i=TCaseIdNode(idt,m.start)$ ;
        Int/i         -> $m=self.mark()$ IntTok/itk $i=IntNode(itk,m.start)$ ;

        # All other terminals are generated by generateTerminals.py and autoappended by compm3parser.py
        # newg.bat should look after this for you
        kwUNSAFE/k -> $m=self.mark()$ 'UNSAFE' $k=KeyWordNode('UNSAFE',m.start)$ ;
        kwINTERFACE/k -> $m=self.mark()$ 'INTERFACE' $k=KeyWordNode('INTERFACE',m.start)$ ;
        kwEND/k -> $m=self.mark()$ 'END' $k=KeyWordNode('END',m.start)$ ;
        kwMODULE/k -> $m=self.mark()$ 'MODULE' $k=KeyWordNode('MODULE',m.start)$ ;
        kwEXPORTS/k -> $m=self.mark()$ 'EXPORTS' $k=KeyWordNode('EXPORTS',m.start)$ ;
        kwGENERIC/k -> $m=self.mark()$ 'GENERIC' $k=KeyWordNode('GENERIC',m.start)$ ;
        kwIMPORT/k -> $m=self.mark()$ 'IMPORT' $k=KeyWordNode('IMPORT',m.start)$ ;
        kwFROM/k -> $m=self.mark()$ 'FROM' $k=KeyWordNode('FROM',m.start)$ ;
        kwBEGIN/k -> $m=self.mark()$ 'BEGIN' $k=KeyWordNode('BEGIN',m.start)$ ;
        kwCONST/k -> $m=self.mark()$ 'CONST' $k=KeyWordNode('CONST',m.start)$ ;
        kwTYPE/k -> $m=self.mark()$ 'TYPE' $k=KeyWordNode('TYPE',m.start)$ ;
        kwEXCEPTION/k -> $m=self.mark()$ 'EXCEPTION' $k=KeyWordNode('EXCEPTION',m.start)$ ;
        kwVAR/k -> $m=self.mark()$ 'VAR' $k=KeyWordNode('VAR',m.start)$ ;
        kwREVEAL/k -> $m=self.mark()$ 'REVEAL' $k=KeyWordNode('REVEAL',m.start)$ ;
        kwAS/k -> $m=self.mark()$ 'AS' $k=KeyWordNode('AS',m.start)$ ;
        kwPROCEDURE/k -> $m=self.mark()$ 'PROCEDURE' $k=KeyWordNode('PROCEDURE',m.start)$ ;
        kwRAISES/k -> $m=self.mark()$ 'RAISES' $k=KeyWordNode('RAISES',m.start)$ ;
        kwVALUE/k -> $m=self.mark()$ 'VALUE' $k=KeyWordNode('VALUE',m.start)$ ;
        kwREADONLY/k -> $m=self.mark()$ 'READONLY' $k=KeyWordNode('READONLY',m.start)$ ;
        kwANY/k -> $m=self.mark()$ 'ANY' $k=KeyWordNode('ANY',m.start)$ ;
        kwCASE/k -> $m=self.mark()$ 'CASE' $k=KeyWordNode('CASE',m.start)$ ;
        kwOF/k -> $m=self.mark()$ 'OF' $k=KeyWordNode('OF',m.start)$ ;
        kwELSE/k -> $m=self.mark()$ 'ELSE' $k=KeyWordNode('ELSE',m.start)$ ;
        kwEXIT/k -> $m=self.mark()$ 'EXIT' $k=KeyWordNode('EXIT',m.start)$ ;
        kwEVAL/k -> $m=self.mark()$ 'EVAL' $k=KeyWordNode('EVAL',m.start)$ ;
        kwFOR/k -> $m=self.mark()$ 'FOR' $k=KeyWordNode('FOR',m.start)$ ;
        kwTO/k -> $m=self.mark()$ 'TO' $k=KeyWordNode('TO',m.start)$ ;
        kwBY/k -> $m=self.mark()$ 'BY' $k=KeyWordNode('BY',m.start)$ ;
        kwDO/k -> $m=self.mark()$ 'DO' $k=KeyWordNode('DO',m.start)$ ;
        kwIF/k -> $m=self.mark()$ 'IF' $k=KeyWordNode('IF',m.start)$ ;
        kwTHEN/k -> $m=self.mark()$ 'THEN' $k=KeyWordNode('THEN',m.start)$ ;
        kwLOCK/k -> $m=self.mark()$ 'LOCK' $k=KeyWordNode('LOCK',m.start)$ ;
        kwLOOP/k -> $m=self.mark()$ 'LOOP' $k=KeyWordNode('LOOP',m.start)$ ;
        kwRAISE/k -> $m=self.mark()$ 'RAISE' $k=KeyWordNode('RAISE',m.start)$ ;
        kwREPEAT/k -> $m=self.mark()$ 'REPEAT' $k=KeyWordNode('REPEAT',m.start)$ ;
        kwUNTIL/k -> $m=self.mark()$ 'UNTIL' $k=KeyWordNode('UNTIL',m.start)$ ;
        kwRETURN/k -> $m=self.mark()$ 'RETURN' $k=KeyWordNode('RETURN',m.start)$ ;
        kwTYPECASE/k -> $m=self.mark()$ 'TYPECASE' $k=KeyWordNode('TYPECASE',m.start)$ ;
        kwTRY/k -> $m=self.mark()$ 'TRY' $k=KeyWordNode('TRY',m.start)$ ;
        kwEXCEPT/k -> $m=self.mark()$ 'EXCEPT' $k=KeyWordNode('EXCEPT',m.start)$ ;
        kwFINALLY/k -> $m=self.mark()$ 'FINALLY' $k=KeyWordNode('FINALLY',m.start)$ ;
        kwWHILE/k -> $m=self.mark()$ 'WHILE' $k=KeyWordNode('WHILE',m.start)$ ;
        kwWITH/k -> $m=self.mark()$ 'WITH' $k=KeyWordNode('WITH',m.start)$ ;
        kwELSIF/k -> $m=self.mark()$ 'ELSIF' $k=KeyWordNode('ELSIF',m.start)$ ;
        kwARRAY/k -> $m=self.mark()$ 'ARRAY' $k=KeyWordNode('ARRAY',m.start)$ ;
        kwBITS/k -> $m=self.mark()$ 'BITS' $k=KeyWordNode('BITS',m.start)$ ;
        kwOBJECT/k -> $m=self.mark()$ 'OBJECT' $k=KeyWordNode('OBJECT',m.start)$ ;
        kwMETHODS/k -> $m=self.mark()$ 'METHODS' $k=KeyWordNode('METHODS',m.start)$ ;
        kwOVERRIDES/k -> $m=self.mark()$ 'OVERRIDES' $k=KeyWordNode('OVERRIDES',m.start)$ ;
        kwRECORD/k -> $m=self.mark()$ 'RECORD' $k=KeyWordNode('RECORD',m.start)$ ;
        kwUNTRACED/k -> $m=self.mark()$ 'UNTRACED' $k=KeyWordNode('UNTRACED',m.start)$ ;
        kwREF/k -> $m=self.mark()$ 'REF' $k=KeyWordNode('REF',m.start)$ ;
        kwSET/k -> $m=self.mark()$ 'SET' $k=KeyWordNode('SET',m.start)$ ;
        kwBRANDED/k -> $m=self.mark()$ 'BRANDED' $k=KeyWordNode('BRANDED',m.start)$ ;
        kwROOT/k -> $m=self.mark()$ 'ROOT' $k=KeyWordNode('ROOT',m.start)$ ;
        kwCAPSULE/k -> $m=self.mark()$ 'CAPSULE' $k=KeyWordNode('CAPSULE',m.start)$ ;
        kwCONNECT/k -> $m=self.mark()$ 'CONNECT' $k=KeyWordNode('CONNECT',m.start)$ ;
        kwPORT/k -> $m=self.mark()$ 'PORT' $k=KeyWordNode('PORT',m.start)$ ;
        kwMESSAGE/k -> $m=self.mark()$ 'MESSAGE' $k=KeyWordNode('MESSAGE',m.start)$ ;
        kwINCOMING/k -> $m=self.mark()$ 'INCOMING' $k=KeyWordNode('INCOMING',m.start)$ ;
        kwOUTGOING/k -> $m=self.mark()$ 'OUTGOING' $k=KeyWordNode('OUTGOING',m.start)$ ;
        kwHANDLER/k -> $m=self.mark()$ 'HANDLER' $k=KeyWordNode('HANDLER',m.start)$ ;
        kwACTIVITY/k -> $m=self.mark()$ 'ACTIVITY' $k=KeyWordNode('ACTIVITY',m.start)$ ;
        kwSEND/k -> $m=self.mark()$ 'SEND' $k=KeyWordNode('SEND',m.start)$ ;
        kwSTATE/k -> $m=self.mark()$ 'STATE' $k=KeyWordNode('STATE',m.start)$ ;
        kwNEXT/k -> $m=self.mark()$ 'NEXT' $k=KeyWordNode('NEXT',m.start)$ ;
        kwTRIGGER/k -> $m=self.mark()$ 'TRIGGER' $k=KeyWordNode('TRIGGER',m.start)$ ;
        kwON/k -> $m=self.mark()$ 'ON' $k=KeyWordNode('ON',m.start)$ ;
        kwSTART/k -> $m=self.mark()$ 'START' $k=KeyWordNode('START',m.start)$ ;
        kwWHEN/k -> $m=self.mark()$ 'WHEN' $k=KeyWordNode('WHEN',m.start)$ ;
        kwCHANGEABLE/k -> $m=self.mark()$ 'CHANGEABLE' $k=KeyWordNode('CHANGEABLE',m.start)$ ;
        kwFIXED/k -> $m=self.mark()$ 'FIXED' $k=KeyWordNode('FIXED',m.start)$ ;
        kwONESHOT/k -> $m=self.mark()$ 'ONESHOT' $k=KeyWordNode('ONESHOT',m.start)$ ;
        kwPERIODIC/k -> $m=self.mark()$ 'PERIODIC' $k=KeyWordNode('PERIODIC',m.start)$ ;
        kwTIMER/k -> $m=self.mark()$ 'TIMER' $k=KeyWordNode('TIMER',m.start)$ ;
        kwDELAY/k -> $m=self.mark()$ 'DELAY' $k=KeyWordNode('DELAY',m.start)$ ;
        kwUSECAPSULE/k -> $m=self.mark()$ 'USECAPSULE' $k=KeyWordNode('USECAPSULE',m.start)$ ;
        kwPYTHON/k -> $m=self.mark()$ 'PYTHON' $k=KeyWordNode('PYTHON',m.start)$ ;
        kwREADS/k -> $m=self.mark()$ 'READS' $k=KeyWordNode('READS',m.start)$ ;
        kwWRITES/k -> $m=self.mark()$ 'WRITES' $k=KeyWordNode('WRITES',m.start)$ ;
        kwSENDS/k -> $m=self.mark()$ 'SENDS' $k=KeyWordNode('SENDS',m.start)$ ;
        kwLIST/k -> $m=self.mark()$ 'LIST' $k=KeyWordNode('LIST',m.start)$ ;
        kwFOREACH/k -> $m=self.mark()$ 'FOREACH' $k=KeyWordNode('FOREACH',m.start)$ ;
        kwDICT/k -> $m=self.mark()$ 'DICT' $k=KeyWordNode('DICT',m.start)$ ;
        kwPROTOCOL/k -> $m=self.mark()$ 'PROTOCOL' $k=KeyWordNode('PROTOCOL',m.start)$ ;
        kwIMPLEMENTS/k -> $m=self.mark()$ 'IMPLEMENTS' $k=KeyWordNode('IMPLEMENTS',m.start)$ ;
        kwSYNCHRONOUS/k -> $m=self.mark()$ 'SYNCHRONOUS' $k=KeyWordNode('SYNCHRONOUS',m.start)$ ;
        kwRESET/k -> $m=self.mark()$ 'RESET' $k=KeyWordNode('RESET',m.start)$ ;
        kwCALL/k -> $m=self.mark()$ 'CALL' $k=KeyWordNode('CALL',m.start)$ ;
        kwSCALED/k -> $m=self.mark()$ 'SCALED' $k=KeyWordNode('SCALED',m.start)$ ;
        kwASSERT/k -> $m=self.mark()$ 'ASSERT' $k=KeyWordNode('ASSERT',m.start)$ ;
        kwAFTER/k -> $m=self.mark()$ 'AFTER' $k=KeyWordNode('AFTER',m.start)$ ;
        kwREPLY/k -> $m=self.mark()$ 'REPLY' $k=KeyWordNode('REPLY',m.start)$ ;
        kwAtoB/k -> $m=self.mark()$ '\-\>' $k=KeyWordNode('->',m.start)$ ;
        kwPortToPort/k -> $m=self.mark()$ '\<\=\>' $k=KeyWordNode('<=>',m.start)$ ;
        kwARROW/k -> $m=self.mark()$ '\=\>' $k=KeyWordNode('=>',m.start)$ ;
        opEQ/k -> $m=self.mark()$ '\=' $k=OpNode('=',m.start)$ ;
        opSUP/k -> $m=self.mark()$ '\<\:' $k=OpNode('<:',m.start)$ ;
        opHASH/k -> $m=self.mark()$ '\#' $k=OpNode('#',m.start)$ ;
        opLTEQ/k -> $m=self.mark()$ '\<\=' $k=OpNode('<=',m.start)$ ;
        opGTEQ/k -> $m=self.mark()$ '\>\=' $k=OpNode('>=',m.start)$ ;
        opLT/k -> $m=self.mark()$ '\<' $k=OpNode('<',m.start)$ ;
        opGT/k -> $m=self.mark()$ '\>' $k=OpNode('>',m.start)$ ;
        opIN/k -> $m=self.mark()$ 'IN' $k=OpNode('IN',m.start)$ ;
        opPLUS/k -> $m=self.mark()$ '\+' $k=OpNode('+',m.start)$ ;
        opAGGR/k -> $m=self.mark()$ '\@' $k=OpNode('@',m.start)$ ;
        opMINUS/k -> $m=self.mark()$ '\-' $k=OpNode('-',m.start)$ ;
        opAMP/k -> $m=self.mark()$ '\&' $k=OpNode('&',m.start)$ ;
        opTIMES/k -> $m=self.mark()$ '\*' $k=OpNode('*',m.start)$ ;
        opDIVIDE/k -> $m=self.mark()$ '\/' $k=OpNode('/',m.start)$ ;
        opDIV/k -> $m=self.mark()$ 'DIV' $k=OpNode('DIV',m.start)$ ;
        opMOD/k -> $m=self.mark()$ 'MOD' $k=OpNode('MOD',m.start)$ ;
        opAND/k -> $m=self.mark()$ 'AND' $k=OpNode('AND',m.start)$ ;
        opNOT/k -> $m=self.mark()$ 'NOT' $k=OpNode('NOT',m.start)$ ;
        opOR/k -> $m=self.mark()$ 'OR' $k=OpNode('OR',m.start)$ ;
        opCARET/k -> $m=self.mark()$ '\^' $k=OpNode('^',m.start)$ ;
        tokLCR/k -> $m=self.mark()$ '\{' $k=TokNode('{',m.start)$ ;
        tokRCR/k -> $m=self.mark()$ '\}' $k=TokNode('}',m.start)$ ;
        tokLBR/k -> $m=self.mark()$ '\(' $k=TokNode('(',m.start)$ ;
        tokRBR/k -> $m=self.mark()$ '\)' $k=TokNode(')',m.start)$ ;
        tokLSQ/k -> $m=self.mark()$ '\[' $k=TokNode('[',m.start)$ ;
        tokRSQ/k -> $m=self.mark()$ '\]' $k=TokNode(']',m.start)$ ;
        tokASS/k -> $m=self.mark()$ '\:\=' $k=TokNode(':=',m.start)$ ;
        tokCOL/k -> $m=self.mark()$ '\:' $k=TokNode(':',m.start)$ ;
        tokTILDE/k -> $m=self.mark()$ '\~' $k=TokNode('~',m.start)$ ;
        tokSEMI/k -> $m=self.mark()$ '\;' $k=SepNode(';',m.start)$ ;
        tokCOMMA/k -> $m=self.mark()$ '\,' $k=SepNode(',',m.start)$ ;
        tokPIPE/k -> $m=self.mark()$ '\|' $k=SepNode('|',m.start)$ ;
        tokDOTDOT/k -> $m=self.mark()$ '\.\.' $k=SepNode('..',m.start)$ ;
        tokDOT/k -> $m=self.mark()$ '\.' $k=SepNode('.',m.start)$ ;

"""
