# $0$ kaccesstype
# $1$ kaddress
# $2$ kmachines
#
procedure Clear_perm(adr: $1$; m: $2$);
begin
  alias l_perm_set:g_perm[m][adr] do
      for acc : $0$ do
        l_perm_set[acc] := false;
      endfor;
  endalias;
end;

procedure Set_perm(acc: $0$; adr: $1$; m: $2$);
begin
  alias l_perm_set:g_perm[m][adr] do
    l_perm_set[acc] := true;
  endalias;
end;

procedure Reset_perm();
begin
  for m:$2$ do
    for adr:$1$ do
      for acc : $0$ do
        g_perm[m][adr][acc] := false;
      endfor;
    endfor;
  endfor;
end;

