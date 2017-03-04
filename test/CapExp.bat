call m3 CapExpTypes.i3 %*
call m3 CapExp.i3 %*
call m3 CapExp.m3 %*
call runcap CapExp --self-congratulate
call runcap CapExp CapExpFail --fail --self-congratulate
