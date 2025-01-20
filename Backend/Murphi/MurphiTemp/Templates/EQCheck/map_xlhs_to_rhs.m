# $0$ lhs object
# $1$ rhs object
#
function map_$0$_to_$1$(m: OBJSET_$0$): OBJSET_$1$
begin
  return from_m_$1$(map_LHS_to_RHS(to_m_$0$(m)));
end;