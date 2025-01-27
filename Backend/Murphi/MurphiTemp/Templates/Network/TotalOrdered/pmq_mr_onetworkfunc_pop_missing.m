# $0$ networkname
# $1$ machines type
# $2$ check, e.g. isElement_$1$(dst)
# $3$ element, e.g. from_m_$1$(dst)
#
if !isundefined(dst.$1$) then
    error "Attempt to pop from queue $0$_$1$, which is not modeled"; 
  els