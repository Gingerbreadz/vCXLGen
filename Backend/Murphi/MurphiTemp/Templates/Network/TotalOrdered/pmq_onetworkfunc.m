# $0$ networkname
# $1$ machines key
# $2$ send_body
# $3$ pop_body
# $4$ send end_body
# $5$ pop end_body
#
procedure Send_$0$(msg:Message; src: $1$;);
begin
  alias dst : msg.dst do
  $2$e
    error "unknown send machine";
  endif;
  $4$
  endalias;
end;

procedure Pop_$0$(dst:$1$; src: $1$;);
begin
  $3$e
    error "unknown pop machine";
  endif;
  $5$
end;