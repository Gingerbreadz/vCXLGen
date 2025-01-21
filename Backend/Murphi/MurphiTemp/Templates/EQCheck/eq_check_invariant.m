liveness "can always switch back to LHS" g_system_state = systemLHS;
liveness "can always switch back to RHS" g_system_state = systemRHS;
liveness "can always track progress" g_system_state = systemRHS & g_progress_tracking;
