# $0$ object name
# $1$ scalarmap
# $2$ object prefix
#
function mapped_$0$(v: i_$1$$0$; m: Machines) : boolean
begin
  for c : $2$$0$ do
    if !isundefined(v[c]) & v[c] = m then
      return true;
    endif;
  endfor;
  return false;
end;

function next_scalar_$0$(v: i_$1$$0$) : Machines
begin
  for m : Machines do
    if isElement_$0$(m) & !mapped_$0$(v, m) then
      return m;
    endif;
  endfor;
  error "next $0$ scalar can not be determined"
end;