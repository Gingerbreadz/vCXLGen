# $0$ Type
# $1$ Channel
# $2$ Instance
# $3$ Unwanted System State
#
if cnt_$1$_$0$[from_m_$0$($2$)] > 0 then
  for idx := 0 to cnt_$1$_$0$[from_m_$0$($2$)]-1 do
    if is_machine_in_state($1$_$0$[from_m_$0$($2$)][idx].src, $3$) then
      return false;
    endif;
  endfor;
endif;