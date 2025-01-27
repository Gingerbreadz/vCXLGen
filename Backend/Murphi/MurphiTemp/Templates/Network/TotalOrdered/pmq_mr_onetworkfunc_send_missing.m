# $0$ networkname
# $1$ machines type
#
if !isundefined(dst.$1$) then
    error "Attempt to send to queue $0$_$1$, which is not modeled"; 
  els