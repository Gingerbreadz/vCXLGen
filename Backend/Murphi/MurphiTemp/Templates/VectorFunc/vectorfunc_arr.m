# $0$ vectorname
# $1$ vectortype
# $2$ machineset
# $3$ vectortyperange
#
-- .add()
procedure AddElement_$0$(var sv:$1$; n:$2$);
begin
    sv[n] := true;
end;

-- .del()
procedure RemoveElement_$0$(var sv:$1$; n:$2$);
begin
    sv[n] := false;
end;

-- .clear()
procedure ClearVector_$0$(var sv:$1$;);
begin
    for n : $2$ do
      sv[n] := false;
    endfor;
end;

-- .contains()
function IsElement_$0$(var sv:$1$; n:$2$) : boolean;
begin
    return sv[n];
end;

-- .count()
function VectorCount_$0$(var sv:$1$) : $3$$1$;
var cnt : $3$$1$;
begin
    cnt := 0;
    for n : $2$ do
      if sv[n] then
        cnt := cnt + 1;
      endif;
    endfor;
    return cnt;
end;

-- .empty()
function HasElement_$0$(var sv:$1$) : boolean;
begin
    return VectorCount_$0$(sv) > 0;
end;
