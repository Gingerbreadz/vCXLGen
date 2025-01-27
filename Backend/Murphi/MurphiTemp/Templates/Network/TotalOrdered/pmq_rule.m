# $0$ networkname
# $1$ machine type
# $2$ conditions
# $3$ element
#
ruleset n:OBJSET_$1$ do
  alias msg:$0$_$1$[n][0] do
    rule "Receive $1$ $0$"
      cnt_$0$_$1$[n] > 0
      $2$
    ==>
      if FSM_MSG_$1$(msg, n) then
        Pop_$0$($3$, $3$);
      endif;
    endrule;
  endalias;
endruleset;