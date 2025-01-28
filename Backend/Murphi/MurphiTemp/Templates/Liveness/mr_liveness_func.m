# $0$ Cache type
#
function live_$0$(adr: Address; acc: PermissionType): boolean
begin
  for n : OBJSET_$0$ do
    if g_perm.$0$[n][adr][acc] then
      return true;
    endif;
  endfor;

  return false;
end;
