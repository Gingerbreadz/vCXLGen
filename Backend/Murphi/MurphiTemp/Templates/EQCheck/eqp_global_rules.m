rule "SWITCH FROM LHS TO RHS"
  g_system_state = systemLHS
  & can_switch_out_of(g_system_state)
  & can_switch_to(systemRHS)
==>
  g_progress_tracking := false;
  g_system_state := systemRHS;
  BackupRHS();
endrule;

rule "SWITCH FROM RHS TO LHS"
  g_system_state = systemRHS
  & can_switch_out_of(g_system_state)
  & can_switch_to(systemLHS)
==>
  g_system_state := systemLHS;
  if !g_progress_tracking then
    BackupRHS();
  else
    if sameOutputOB() then
      g_progress_tracking := false;
    endif;
    RestoreRHSBackup();
  endif;
endrule;

rule "SWITCH FROM LHS TO LHSEXT"
  g_system_state = systemLHS
  & can_switch_out_of(g_system_state)
  & can_switch_to(systemLHSExt)
==>
  g_system_state := systemLHSExt;
  BackupRHS();
endrule;

rule "SWITCH FROM LHSEXT TO LHS"
  g_system_state = systemLHSExt
  & can_switch_out_of(g_system_state)
  & can_switch_to(systemLHS)
==>
  g_system_state := systemLHS;
  BackupRHS();
endrule;

rule "Track Progress"
  g_system_state = systemLHS
  & sameOutputOB()
  & !g_progress_tracking
==>
  g_system_state := systemRHS;
  g_progress_tracking := true;
endrule;

rule "RESET RHS"
  g_system_state = systemRHS
==>
  RestoreRHSBackup()
endrule;