function map_LHS_to_RHS(m: Machines): Machines
var ret: Machines;
begin
  undefine ret;
  if !isundefined(m.$1$) then
    ret.$2$ := $2$;
    return ret;
  endif; 
$0$
  
  return ret;
end;