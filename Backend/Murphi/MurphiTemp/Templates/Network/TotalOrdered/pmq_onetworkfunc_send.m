# $0$ networkname
# $1$ machines type
# $2$ check, e.g. isElement_$1$(dst)
# $3$ element, e.g. from_m_$1$(dst)
#
if $2$ then
    Assert(cnt_$0$_$1$[$3$] < O_NET_MAX) "Too many messages: $0$_$1$";
    $0$_$1$[$3$][cnt_$0$_$1$[$3$]] := msg;
    cnt_$0$_$1$[$3$] := cnt_$0$_$1$[$3$] + 1;
  els