function map_LHS_msg_to_RHS(lhs_m: Message): Message;
var rhs_m: Message
begin

  if isundefined(lhs_m.adr) then
    undefine rhs_m.adr;
  else
    rhs_m.adr := lhs_m.adr;
  endif;
  if isundefined(lhs_m.mtype) then
    undefine rhs_m.mtype;
  else
    rhs_m.mtype := lhs_m.mtype;
  endif;
  undefine rhs_m.src;
  rhs_m.src := map_LHS_to_RHS(lhs_m.src);
  undefine rhs_m.dst;
  rhs_m.dst := map_LHS_to_RHS(lhs_m.dst);
  if isundefined(lhs_m.acksExpectedL1) then
    undefine rhs_m.acksExpectedL1;
  else
    rhs_m.acksExpectedL1 := lhs_m.acksExpectedL1;
  endif;
  if isundefined(lhs_m.acksExpectedL2) then
    undefine rhs_m.acksExpectedL2;
  else
    rhs_m.acksExpectedL2 := lhs_m.acksExpectedL2;
  endif;
  if isundefined(lhs_m.cl) then
    undefine rhs_m.cl;
  else
    rhs_m.cl := lhs_m.cl;
  endif;

  return rhs_m;
end;

function is_LHS_msg_eq_RHS(lhs_m: Message; rhs_m: Message): boolean;
begin
  
  if isundefined(lhs_m.adr) & !isundefined(rhs_m.adr) then
    return false;
  elsif !isundefined(lhs_m.adr) & isundefined(rhs_m.adr) then
    return false; 
  elsif !isundefined(lhs_m.adr) & !isundefined(rhs_m.adr)  then
    if lhs_m.adr != rhs_m.adr then
      return false;
    endif;
  endif;
  
  if isundefined(lhs_m.mtype) & !isundefined(rhs_m.mtype) then
    return false;
  elsif !isundefined(lhs_m.mtype) & isundefined(rhs_m.mtype) then
    return false; 
  elsif !isundefined(lhs_m.mtype) & !isundefined(rhs_m.mtype)  then
    if lhs_m.mtype != rhs_m.mtype then
      return false;
    endif;
  endif;
  
  if map_LHS_to_RHS(lhs_m.src) != rhs_m.src then
    return false;
  endif;
  
  if map_LHS_to_RHS(lhs_m.dst) != rhs_m.dst then
    return false;
  endif;
  
  if isundefined(lhs_m.acksExpectedL1) & !isundefined(rhs_m.acksExpectedL1) then
    return false;
  elsif !isundefined(lhs_m.acksExpectedL1) & isundefined(rhs_m.acksExpectedL1) then
    return false; 
  elsif !isundefined(lhs_m.acksExpectedL1) & !isundefined(rhs_m.acksExpectedL1)  then
    if lhs_m.acksExpectedL1 != rhs_m.acksExpectedL1 then
      return false;
    endif;
  endif;

  if isundefined(lhs_m.acksExpectedL2) & !isundefined(rhs_m.acksExpectedL2) then
    return false;
  elsif !isundefined(lhs_m.acksExpectedL2) & isundefined(rhs_m.acksExpectedL2) then
    return false; 
  elsif !isundefined(lhs_m.acksExpectedL2) & !isundefined(rhs_m.acksExpectedL2)  then
    if lhs_m.acksExpectedL2 != rhs_m.acksExpectedL2 then
      return false;
    endif;
  endif;
  
  if isundefined(lhs_m.cl) & !isundefined(rhs_m.cl) then
    return false;
  elsif !isundefined(lhs_m.cl) & isundefined(rhs_m.cl) then
    return false; 
  elsif !isundefined(lhs_m.cl) & !isundefined(rhs_m.cl)  then
    if lhs_m.cl != rhs_m.cl then
      return false;
    endif;
  endif;

  return true;
end;