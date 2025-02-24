# $0$ networkname
# $1$ machine type
#
ruleset dst:OBJSET_$1$ do
    choose midx:$0$_$1$[dst] do
        alias mach:$0$_$1$[dst] do
        alias msg:mach[midx] do
            rule "Receive $0$_$1$"
            !isundefined(msg.mtype)
            ==>
            if FSM_MSG_$1$(msg, dst) then
                MultiSetRemove(midx, mach);
            endif;    
            endrule;
        endalias;
        endalias;
    endchoose;
endruleset;