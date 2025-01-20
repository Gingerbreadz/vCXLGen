# $0$ src-Type
# $1$ dst-Type
# $2$ src
# $3$ dst
# $4$ Channel
# $5$ Mapping Function (if needed)
#
undefine $4$_$1$[$3$];
cnt_$4$_$1$[$3$] := cnt_$4$_$0$[$2$];
if cnt_$4$_$0$[$2$] > 0 then
  for idx := 0 to cnt_$4$_$0$[$2$]-1 do  
    $4$_$1$[$3$][idx] := $5$($4$_$0$[$2$][idx]);
  endfor;
endif;