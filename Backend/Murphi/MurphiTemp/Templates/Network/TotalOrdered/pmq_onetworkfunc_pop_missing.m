# $0$ networkname
# $1$ machines type
#
if isElement_$1$(dst) then
    error "Attempt to pop from queue $0$_$1$, which is not modeled"; 
  els