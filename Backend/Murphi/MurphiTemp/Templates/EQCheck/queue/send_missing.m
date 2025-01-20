# $0$ lhs-Type
# $1$ rhs-Type
# $2$ Other System State LHS
# $3$ Other System State RHS
# $4$ Channel
#
lhs_offset := 0;
rhs_offset := 0;
#
# if the LHS has msg go over each one of them
#
if cnt_$4$_$0$[elem] > 0 then
  for idx := 0 to cnt_$4$_$0$[elem]-1 do
#
# if the current msg is sent by someone we care about (§2§), then check if RHS has it too
#
    if is_machine_in_state($4$_$0$[elem][idx].src, $2$) then
#
# Skip all elements on the RHS that are not from someone we care about on the RHS ($3$)
#  
      if cnt_$4$_$1$[map_$0$_to_$1$(elem)] <= (idx - lhs_offset + rhs_offset) then
        Send_$4$(map_LHS_msg_to_RHS($4$_$0$[elem][idx]), map_LHS_to_RHS($4$_$0$[elem][idx].src));
      endif;
      while !is_machine_in_state($4$_$1$[map_$0$_to_$1$(elem)][idx - lhs_offset + rhs_offset].src, $3$) do
        rhs_offset := rhs_offset + 1;
        if cnt_$4$_$1$[map_$0$_to_$1$(elem)] <= (idx - lhs_offset + rhs_offset) then
          Send_$4$(map_LHS_msg_to_RHS($4$_$0$[elem][idx]), map_LHS_to_RHS($4$_$0$[elem][idx].src));
        endif;
      endwhile;
#
# If the messages are not the same then abort, since we found a problem
#
      if !is_LHS_msg_eq_RHS($4$_$0$[elem][idx], $4$_$1$[map_$0$_to_$1$(elem)][idx - lhs_offset + rhs_offset]) then
          error "Replication $0$ -> $1$ for queue $4$ failed : Mismatch";
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
# If the RHS still has more msg in it's queue, ensure that we do not care about any of them
#
if cnt_$4$_$1$[map_$0$_to_$1$(elem)] > (cnt_$4$_$0$[elem] - lhs_offset + rhs_offset) then
  for idx := (cnt_$4$_$0$[elem] - lhs_offset + rhs_offset) to cnt_$4$_$1$[map_$0$_to_$1$(elem)]-1 do
    if is_machine_in_state($4$_$1$[map_$0$_to_$1$(elem)][idx].src, $3$) then
      error "Replication $0$ -> $1$ for queue $4$ failed : Too Many";
    endif;
  endfor;
endif;
