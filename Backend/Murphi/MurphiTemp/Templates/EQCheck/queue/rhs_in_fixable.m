# $0$ lhs-Type
# $1$ rhs-Type
# $2$ Other System State LHS
# $3$ Other System State RHS
# $4$ Channel
#
lhs_offset := 0;
rhs_offset := 0;
alias elem_rhs : map_$0$_to_$1$(elem) do
#
# if the LHS has msg go over each one of them (in reverse order)
#
  if cnt_$4$_$0$[elem] > 0 then
    for idx := 0 to cnt_$4$_$0$[elem]-1 do
#
# if the current msg is sent by someone we care about (§2§), then check if RHS has it to
#
      if is_machine_in_state($4$_$0$[elem][cnt_$4$_$0$[elem]-1 - idx].src, $2$) then
#
# Skip all elements on the RHS that are not from someone we care about on the RHS ($3$)
#  
        if cnt_$4$_$1$[elem_rhs] <= (idx - lhs_offset + rhs_offset) then
          return false;
        endif;
        while !is_machine_in_state($4$_$1$[elem_rhs][cnt_$4$_$1$[elem_rhs]-1 - (idx - lhs_offset + rhs_offset)].src, $3$) do
          rhs_offset := rhs_offset + 1;
          if cnt_$4$_$1$[elem_rhs] <= (idx - lhs_offset + rhs_offset) then
            return false;
          endif;
        endwhile;
#
# If the messages are not the same then abort, since we found a problem (RHS processed too much)
#
        if !is_LHS_msg_eq_RHS($4$_$0$[elem][cnt_$4$_$0$[elem]-1 - idx], $4$_$1$[elem_rhs][cnt_$4$_$1$[elem_rhs]-1 - (idx - lhs_offset + rhs_offset)]) then
            return false;
        endif;
      else
#
# If the LHS contained a msg we do not care about, denote the offset so we know what we compare against
#
          lhs_offset := lhs_offset + 1;
      endif;
    endfor;
  endif;
#
# If the RHS still has more msg in it's queue, thats fine, since the RHS can process them
#
endalias;