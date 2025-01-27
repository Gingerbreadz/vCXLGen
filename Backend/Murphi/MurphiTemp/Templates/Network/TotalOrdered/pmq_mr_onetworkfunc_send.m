# $0$ networkname
# $1$ machines type
#
if !isundefined(dst.$1$) then
    Assert(cnt_$0$_$1$[dst.$1$] < O_NET_MAX) "Too many messages: $0$_$1$";
    $0$_$1$[dst.$1$][cnt_$0$_$1$[dst.$1$]] := msg;
    cnt_$0$_$1$[dst.$1$] := cnt_$0$_$1$[dst.$1$] + 1;
  els