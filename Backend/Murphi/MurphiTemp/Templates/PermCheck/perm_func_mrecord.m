# $0$ kaccesstype
# $1$ kaddress
# $2$ kmachines
#
procedure Clear_perm(adr: $1$; m: $2$);
begin
  for acc : $0$ do
$3$
  endfor;
end;

procedure Set_perm(acc: $0$; adr: $1$; m: $2$);
begin
$4$
end;

procedure Reset_perm();
begin
  for acc : $0$ do
    for adr : $1$ do
$5$
    endfor;
  endfor;
end;

