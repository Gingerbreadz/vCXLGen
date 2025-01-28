# $0$ Type
#
#
function active_$0$(m: OBJSET_$0$; adr: Address): boolean;
begin

  for n : OBJSET_$0$ do
    if n != m then
      if $1$ != $2$ then
        return false;
      endif;
    endif;
  endfor;

  return true;
end;