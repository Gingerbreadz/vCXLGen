# $0$ networkname
# $1$ machines type
#
if !isundefined(dst.$1$) then
    Assert (cnt_$0$_$1$[dst.$1$] > 0) "Trying to advance empty queue: $0$_$1$";
    for i := 0 to cnt_$0$_$1$[dst.$1$]-1 do
      if i < cnt_$0$_$1$[dst.$1$]-1 then
        $0$_$1$[dst.$1$][i] := $0$_$1$[dst.$1$][i+1];
      else
        undefine $0$_$1$[dst.$1$][i];
      endif;
    endfor;
    cnt_$0$_$1$[dst.$1$] := cnt_$0$_$1$[dst.$1$] - 1;
  els