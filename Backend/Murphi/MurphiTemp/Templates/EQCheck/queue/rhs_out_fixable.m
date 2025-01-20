# $0$ lhs-Type
# $1$ rhs-Type
# $2$ Other System State LHS
# $3$ Other System State RHS
# $4$ Channel
#
rhs_offset := 0;
lhs_offset := 0;
alias elem_rhs : map_$0$_to_$1$(elem) do
#
# if the RHS has msg go over each one of them
#
    if cnt_$4$_$1$[elem_rhs] > 0 then
    for idx := 0 to cnt_$4$_$1$[elem_rhs]-1 do
#
# if the current msg is sent by someone we care about ($3$), then check if LHS has it too
#
        if is_machine_in_state($4$_$1$[elem_rhs][idx].src, $3$) then
#
# Skip all msg on the LHS that are not from someone we care about on the LHS ($2$)
#  
        if cnt_$4$_$0$[elem] <= (idx - rhs_offset + lhs_offset) then
            return false;
        endif;
        while !is_machine_in_state($4$_$0$[elem][idx - rhs_offset + lhs_offset].src, $2$) do
            lhs_offset := lhs_offset + 1;
            if cnt_$4$_$0$[elem] <= (idx - rhs_offset + lhs_offset) then
              return false;
            endif;
        endwhile;
#
# If the messages are not the same then abort, since we found a problem
#
        if !is_LHS_msg_eq_RHS($4$_$0$[elem][idx - rhs_offset + lhs_offset], $4$_$1$[elem_rhs][idx]) then
            return false;
        endif;
        else
#
# If the RHS contained a msg we do not care about, denote the offset so we know what we compare against
#
            rhs_offset := rhs_offset + 1;
        endif;
    endfor;
    endif;
#
# If the LHS still has more msg in it's queue, thats fine, since the RHS can add new messages to the queue
#
endalias;