# $0$ RHS restrictions
# $1$ Same OB function 
# $2$ can switch out of LHS
#
function can_switch_out_of(state : SystemStates) : boolean;
begin
  if state = systemLHS then
    return $2$;
  elsif state = systemRHS then
    return $1$() $0$;
  elsif state = systemLHSExt then
    return true;
  elsif state = systemRHSExt then
    error "unreachable system state";
  else
    error "unkown system state";
  endif;
end;

function can_switch_to(state : SystemStates) : boolean;
begin
  if state = systemLHS then
    return true;
  elsif state = systemRHS then
    return !$1$();
  elsif state = systemLHSExt then
    return $1$();
  elsif state = systemRHSExt then
    error "unreachable system state";
  else
    error "unkown system state";
  endif;
end;

function continue_run(machine_state: SystemStates; state: SystemStates) : boolean;
begin
  if machine_state = state then
    if state = systemLHS then
        return !(can_switch_to(systemRHS) & can_switch_out_of(state));
    elsif state = systemRHS then
        return !(can_switch_to(systemLHS) & can_switch_out_of(state)) & can_RHS_replicate_OB();
    elsif state = systemLHSExt then
        return $1$();
    elsif state = systemRHSExt then
        error "unreachable system state";
    else
        error "unkown system state";
    endif;
  else
    return false;
  endif;
end;

