# $0$ networkname
# $1$ machines type
#
if isElement_$1$(msg.dst) then
    Assert (cnt_$0$_$1$[from_m_$1$(dst)] > 0) "Trying to advance empty queue";
    for i := 0 to cnt_$0$_$1$[from_m_$1$(dst)]-1 do
      if i < cnt_$0$_$1$[from_m_$1$(dst)]-1 then
        $0$_$1$[from_m_$1$(dst)][i] := $0$_$1$[from_m_$1$(dst)][i+1];
      else
        undefine $0$_$1$[from_m_$1$(dst)][i];
      endif;
    endfor;
    cnt_$0$_$1$[from_m_$1$(dst)] := cnt_$0$_$1$[from_m_$1$(dst)] - 1;
  els