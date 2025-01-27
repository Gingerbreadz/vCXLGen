# $0$ networkname
# $1$ machines type
# $2$ check, e.g. isElement_$1$(dst)
# $3$ element, e.g. from_m_$1$(dst)
#
if $2$ then
    Assert (cnt_$0$_$1$[$3$] > 0) "Trying to advance empty queue: $0$_$1$";
    for i := 0 to cnt_$0$_$1$[$3$]-1 do
      if i < cnt_$0$_$1$[$3$]-1 then
        $0$_$1$[$3$][i] := $0$_$1$[$3$][i+1];
      else
        undefine $0$_$1$[$3$][i];
      endif;
    endfor;
    cnt_$0$_$1$[$3$] := cnt_$0$_$1$[$3$] - 1;
  els