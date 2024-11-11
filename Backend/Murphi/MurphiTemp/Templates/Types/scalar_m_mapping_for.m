# $0$ object name
# $1$ object prefix
# $2$ scalarmap
#
for o : $1$$0$ do
  if i_$2$$0$[o] = m then
    return o;
  endif;
endfor;
error "can not map from m_$0$"