# $0$ networkname
# $1$ machines type
#
if isElement_$1$(msg.dst) then
    Assert(cnt_$0$_$1$[from_m_$1$(msg.dst)] < O_NET_MAX) "Too many messages: $0$_$1$";
    $0$_$1$[from_m_$1$(msg.dst)][cnt_$0$_$1$[from_m_$1$(msg.dst)]] := msg;
    cnt_$0$_$1$[from_m_$1$(msg.dst)] := cnt_$0$_$1$[from_m_$1$(msg.dst)] + 1;
  els