# $0$ networkname
# $1$ machines type
#
if isElement_$1$(msg.dst) then
    error "Attempt to send to queue $0$_$1$, which is not modeled"; 
  els