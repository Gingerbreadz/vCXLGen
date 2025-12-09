#  Copyright (c) 2021.  Nicolai Oswald
#  Copyright (c) 2021.  University of Edinburgh
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met: redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer;
#  redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution;
#  neither the name of the copyright holders nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


class MurphiTemplates:

    f_template_dir = "Templates"
    f_forbidden = "Forbidden.m"

    f_tmp_make = "MakeFile/tmpmakefile"
    f_license = "license.m"

    f_const = "const.m"

    f_fifo = "FIFO/fifo.m"
    f_fifo_func = "FIFO/fifofunc.m"
    f_fifo_ruleset = "FIFO/FIFORuleset/fiforuleset.m"
    f_fifo_inner_rule = "FIFO/FIFORuleset/fifoinnerrule.m"

    f_perm_obj_mrecord = "PermCheck/perm_obj_mrecord.m"
    f_perm_func_mrecord = "PermCheck/perm_func_mrecord.m"
    f_perm_obj_arr = "PermCheck/perm_obj_arr.m"
    f_perm_func_arr = "PermCheck/perm_func_arr.m"
    f_perm_obj = "PermCheck/perm_obj.m"
    f_perm_func = "PermCheck/perm_func.m"
    f_perm_var = "PermCheck/perm_var.m"

    f_store_monitor_obj = "StoreFunction/GlobalStoreMonitor/GlobalStoreObj.m"
    f_store_monitor_var = "StoreFunction/GlobalStoreMonitor/GlobalStoreVar.m"
    f_store_monitor_func = "StoreFunction/GlobalStoreMonitor/GlobalStoreFunc.m"

    f_store_func = "StoreFunction/StoreFunc.m"

    f_prefetch_phase_function = "LitmusTemp/PrefetchingPhase.m"

    f_pmq_tot_o_network_func = "Network/TotalOrdered/pmq_onetworkfunc.m"
    f_pmq_tot_o_network_func_send = "Network/TotalOrdered/pmq_onetworkfunc_send.m"
    f_pmq_tot_o_network_func_pop = "Network/TotalOrdered/pmq_onetworkfunc_pop.m"
    f_pmq_tot_o_network_func_send_missing = "Network/TotalOrdered/pmq_onetworkfunc_send_missing.m"
    f_pmq_tot_o_network_func_pop_missing = "Network/TotalOrdered/pmq_onetworkfunc_pop_missing.m"
    f_pmq_tot_o_network_ready = "Network/TotalOrdered/pmq_onetworkready.m"
    f_pmq_tot_o_rule = "Network/TotalOrdered/pmq_rule.m"
    f_pmq_u_rule = "Network/Unordered/pmq_rule.m"

    f_pmq_tot_o_mr_func_send = "Network/TotalOrdered/pmq_mr_onetworkfunc_send.m"
    f_pmq_tot_o_mr_func_pop = "Network/TotalOrdered/pmq_mr_onetworkfunc_pop.m"
    f_pmq_tot_o_mr_func_send_missing = "Network/TotalOrdered/pmq_mr_onetworkfunc_send_missing.m"
    f_pmq_tot_o_mr_func_pop_missing = "Network/TotalOrdered/pmq_mr_onetworkfunc_pop_missing.m"

    f_ordered_network_func = "Network/Ordered/onetworkfunc.m"
    f_ordered_network_ready_func = "Network/Ordered/onetworkready.m"
    f_ordered_rule = "Network/Ordered/orderedrule.m"
    f_ordered_rule_inner = "Network/Ordered/orderedinnerrule.m"
    f_ordered_rule_fifo = "Network/Ordered/orderedfifo.m"
    f_ordered_reset = "Network/Ordered/OrderedReset.m"

    f_total_ordered_network_func = "Network/TotalOrdered/onetworkfunc.m"
    f_total_ordered_network_ready_func = "Network/TotalOrdered/onetworkready.m"
    f_total_ordered_rule = "Network/TotalOrdered/orderedrule.m"
    f_total_ordered_reset = "Network/TotalOrdered/OrderedReset.m"

    f_unordered_network_func = "Network/Unordered/unetworkfunc.m"
    f_unordered_network_ready_func = "Network/Unordered/unetworkready.m"
    f_unordered_rule = "Network/Unordered/unorderedrule.m"
    f_unordered_rule_inner = "Network/Unordered/unorderedinnerrule.m"
    f_unordered_rule_fifo = "Network/Unordered/unorderedfifo.m"
    f_unordered_reset = "Network/Unordered/UnorderedReset.m"

    f_network_ready_outer = "Network/network_ready_func_outer.m"
    f_network_ready_inner = "Network/network_ready_func_inner.m"

    f_no_fifo = "Network/nofifo.m"

    f_multicast_network_func = "Network/multicastfunc.m"
    f_multicast_network_func_arr = "Network/multicastfunc_arr.m"
    f_multicast_network_func_mrecord = "Network/multicastfunc_mrecord.m"
    f_broadcast_network_func = "Network/broadcastfunc.m"

    f_vector_func = "VectorFunc/vectorfunc.m"
    f_vector_func_arr = "VectorFunc/vectorfunc_arr.m"
    f_vector_func_mrecord = "VectorFunc/vectorfunc_mrecord.m"

    f_access_rule_set = "RuleSet/AccessHandling/AccessRuleSet.m"
    f_access_rule = "RuleSet/AccessHandling/AccessRule.m"

    f_init_event_rule = "RuleSet/InitEvent/TestAndServeInitEventRule.m"
    f_remote_event_rule = "RuleSet/RemoteEvent/TestRemoteEventRule.m"

    f_remote_event_serve_func = "RuleSet/RemoteEvent/ServeRemoteEvent.m"

    # Types
    f_is_element = "Types/is_element.m"
    f_m_mappings = "Types/m_mappings.m"
    f_scalar_mapping = "Types/scalar_mapping.m"
    f_scalar_m_mapping_for = "Types/scalar_m_mapping_for.m"

    # EQ Check
    f_eq_mappings = "EQCheck/map_lhs_to_rhs_outer.m"
    f_eq_mappings_inner = "EQCheck/map_lhs_to_rhs_inner.m"
    f_eq_x_mappings = "EQCheck/map_xlhs_to_rhs.m"
    f_eq_msg_func = "EQCheck/eq_msg_func.m"
    f_eq_global_state = "EQCheck/eq_global_state.m"
    f_eq_global_rules = "EQCheck/eq_global_rules.m"
    f_eq_global_state_association = "EQCheck/global_state_association.m"
    f_eq_check_invariant = "EQCheck/eq_check_invariant.m"
    f_eq_same_ob = "EQCheck/eq_check_same_ob.m"

    f_eqp_global_state = "EQCheck/eqp_global_state.m"
    f_eqp_global_rules = "EQCheck/eqp_global_rules.m"

    f_eq_mr_global_state = "EQCheck/eq_MR_global_state.m"
    f_eqp_mr_global_state = "EQCheck/eqp_MR_global_state.m"

    f_eq_mr_mappings = "EQCheck/map_MR_lhs_to_rhs_outer.m"
    f_eq_mr_mappings_inner = "EQCheck/map_MR_lhs_to_rhs_inner.m"
    f_eq_mr_msg_func = "EQCheck/eq_MR_msg_func.m"
    f_eq_mr_queue_no_msg_from = "EQCheck/queue/MR_no_msg_from.m"
    f_eq_mr_rhs_l1_only_one_active = "EQCheck/eq_MR_rhs_l1_only_one_active.m"

    f_eq_queue_equal = "EQCheck/queue/equal.m"
    f_eq_queue_in_fixable = "EQCheck/queue/rhs_in_fixable.m"
    f_eq_queue_out_fixable = "EQCheck/queue/rhs_out_fixable.m"
    f_eq_queue_copy = "EQCheck/queue/copy.m"
    f_eq_queue_send_missing = "EQCheck/queue/send_missing.m"
    f_eq_queue_no_msg_from = "EQCheck/queue/no_msg_from.m"

    f_access_based_liveness = "Liveness/access_based_liveness.m"
    f_mr_access_based_liveness = "Liveness/mr_access_based_liveness.m"
    f_mr_access_based_liveness_scalar = "Liveness/mr_access_based_liveness_scalar.m"
    f_mr_liveness_func = "Liveness/mr_liveness_func.m"

    # Reset functions
    f_machine_reset_body = "ResetFunc/MachineResetBody.m"
    f_fifo_reset_body = "ResetFunc/ResetBody.m"
    f_fifo_reset_inner = "ResetFunc/FIFOResetInner.m"

    # Invariants
    f_invariant_SW = "Invariants/invariantSW.m"     # Single writer
    f_invariant_EW = "Invariants/invariantEW.m"     # Exclusive writer

    # Litmus Templates
    f_cpuinstancegen = "LitmusTemp/CPUdefinition.m"
    f_cpubufferfunc = "LitmusTemp/CPUbufferfunc.m"

    # Litmus Trace Templates
    f_inactive_cpu = "LitmusTemp/InactiveCPU.m"
    f_cpu_cache_map_init = "LitmusTemp/CPUcachemap_init.m"
    f_cpu_cache_map_body = "LitmusTemp/CPUcachemap_body.m"

    f_cpu_cache_access_head = "LitmusTemp/CPUAccessCache/Access/CPUcacheaccess_head.m"
    f_cpu_cache_access_body = "LitmusTemp/CPUAccessCache/Access/CPUcacheaccess_body.m"
    f_cpu_cache_access_tail = "LitmusTemp/CPUAccessCache/Access/CPUcacheaccess_tail.m"

    f_cpu_try_access = "LitmusTemp/CPUtryaccess.m"
    f_cpu_dummy_access = "LitmusTemp/CPUdummyaccess.m"
    f_cpu_issue_head = "LitmusTemp/CPUAccessCache/Execute_CPU/CPUissue_head.m"
    f_cpu_issue_body = "LitmusTemp/CPUAccessCache/Execute_CPU/CPUissue_body.m"

    f_cpu_serve_head = "LitmusTemp/CPUAccessCache/Execute_CPU/CPUserve_head.m"
    f_cpu_serve_body = "LitmusTemp/CPUAccessCache/Execute_CPU/CPUserve_body.m"

    f_cpu_check_reset = "LitmusTemp/CPUcheckreset.m"
    f_cpu_reset_func = "LitmusTemp/CPUresetfunc.m"

    f_cpu_run_rule = "LitmusTemp/CPUrunrule.m"

    # Litmus Test Frameworks
    f_instr_seq_body = "LitmusTemp/InstrSequence/InstrBody.m"
    f_instr_seq_frame = "LitmusTemp/InstrSequence/InstrSeqFrame.m"
    f_instr_seq_var_body = "LitmusTemp/InstrSequence/InstrVarBody.m"

    f_instr_cond_body = "LitmusTemp/Forbidden/CondCheckBody.m"
    f_instr_cond_frame = "LitmusTemp/Forbidden/CondCheckFrame.m"

    ## Events
    f_event_queue_def = "Event/EventQueueDef.m"
    f_event_func_general = "Event/GeneralEvent.m"
    f_event_queue_def_noms = "Event/EventQueueDef_noms.m"
    f_event_func_general_noms = "Event/GeneralEvent_noms.m"
    f_reset_func = "ResetFunc/ResetFunc.m"
    f_scalar_mapping_reset = "ResetFunc/scalar_mapping_reset.m"
