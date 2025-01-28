# $0$ left hand side entity
# $1$ right hand side entity
#
if !isundefined(m.$0$) then
  ret.$1$ := m.$0$;
  return ret;
endif;