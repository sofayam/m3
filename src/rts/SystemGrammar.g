separator comment:     '\(\*.*?\*\)' ;
separator white:       '[ \r\f\v\t\n]' ;
token     numval:    '\d+(\.\d+)?' float ;
token     Id:          '\w+' ;

START/s -> architecture/s
        | mapping/s;

architecture/a  -> 'SYSTEM' 'ARCHITECTURE' Id/id 'IS' processors/ps links/ls 
                   $a={'id': id, 'processors':ps, 'links': ls}$ 'END' ('\.')? ;

processors/ps   -> $ps=[]$ (processor/p ('\;')? $ps.append(p)$)*;

processor/p     -> 'PROCESSOR' Id/id ('SPEED' numval/n | $n=1.0$) $p=(id,n)$;

links/ls        -> $ls=[]$ (link/l ('\;')? $ls.append(l)$)*;

link/l          -> 'LINK' Id/id1 ('\-\>' $both=False$| '\<\=\>' $both=True$) Id/id2 ('COST' numval/c Id/id) $l=(id1,id2,both,c,id)$;

mapping/m       -> 'SYSTEM' Id/id1 'USING' Id/id2 'IS' allocations/as  
                   $m={'mapid':id1,'sysid':id2,'allocations':as}$ 'END' ('\.')?;

allocations/as  -> $as=[]$ (allocation/a ('\;')? $as.append(a)$)*;

allocation/a    -> 'CAPSULE' capsuleId/capId 'ON' 'PROCESSOR' Id/procId $a=(capId,procId)$;

capsuleId/capId ->  Id/id $capId=[id]$ ('\.' Id/id $capId.append(id)$)*;
