call m3 CapSwapper.i3 %*
call m3 CapStandard.i3 %*
call m3 CapSwapper.m3 %*
call m3 CapStandard.m3 %*
call m3 CapSpecial.m3 %*
call runcap CapSwapper CapStandard 
call runcap CapSwapper CapSpecialGlob --gi=CapStandard=CapSpecial
call runcap CapSwapper CapSpecialInst --ii=top.kid=CapSpecial