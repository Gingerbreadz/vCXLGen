# $0$ prefetching count
function InPrefetchingPhase(): boolean;
begin

  for cpu : OBJSET_CPU do
    if i_cpu[cpu].instrstr.QueueInd < $0$ then
      return true;
    endif;
  endfor;

  return false;
end;