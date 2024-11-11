# $0$ networkname
# $1$ machines key
# $2$ send_body
# $3$ pop_body
#
procedure Send_$0$(msg:Message; src: $1$;);
  $2$e
    error "unknown send machine";
  endif;
end;

procedure Pop_$0$(dst:$1$; src: $1$;);
begin
  $3$e
    error "unknown pop machine";
  endif;
end;