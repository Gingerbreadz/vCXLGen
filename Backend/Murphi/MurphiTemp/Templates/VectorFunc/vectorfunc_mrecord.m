# $0$ vectorname
# $1$ vectortype
# $2$ machineset
# $3$ vectortyperange
#
-- .add()
procedure AddElement_$0$(var sv:$1$; n:$2$);
begin
$4$
end;

-- .del()
procedure RemoveElement_$0$(var sv:$1$; n:$2$);
begin
$5$
end;

-- .clear()
procedure ClearVector_$0$(var sv:$1$;);
begin
$6$
end;

-- .contains()
function IsElement_$0$(sv:$1$; n:$2$) : boolean;
begin
$7$
  return false;
end;

-- .count()
function VectorCount_$0$(sv:$1$) : $3$$1$;
var cnt : $3$$1$;
begin
  cnt := 0;
$8$
  return cnt;
end;

-- .empty()
function HasElement_$0$(sv:$1$) : boolean;
begin
    return VectorCount_$0$(sv) > 0;
end;
