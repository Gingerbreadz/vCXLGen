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

from typing import List, Dict

from Backend.Murphi.MurphiModular.EqCheckHelper import EqCheckHelper
from Backend.Murphi.MurphiModular.OptimizationHelper import OptimizationHelper
from DataObjects.ClassCluster import Cluster

from Backend.Murphi.BaseConfig import BaseConfig
from Backend.Murphi.MurphiModular.MurphiTokens import MurphiTokens
from Backend.Common.TemplateHandler.TemplateHandler import TemplateHandler
from Backend.Murphi.MurphiTemp.TemplateHandler.MurphiTemplates import MurphiTemplates

from Debug.Monitor.ClassDebug import Debug


class GenEQCheckComparisonFunc(TemplateHandler, Debug):

    def __init__(self, murphi_str: List[str], clusters: List[Cluster], config: BaseConfig):
        TemplateHandler.__init__(self)
        Debug.__init__(self)

        functions = "----" + __name__.replace('.','/') + self.nl

        systemStates = ["systemLHS", "systemRHS", "systemLHSExt", "systemRHSExt"]
        machines = EqCheckHelper.get_machines(clusters)
        machineTypes = EqCheckHelper.get_machine_types(clusters)
        systemStateAssoc = EqCheckHelper.get_state_assoc(systemStates, machines, config)

        # template = MurphiTemplates.f_eq_global_state_association
        # functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
        #                                                   [self.gen_state_assoc(systemStates, systemStateAssoc, config)]), 1) + self.nl

        # Message Comparison
        # functions += self.tab + "----" + __name__.replace('.','/') +  " : MessageComparisonFunctions" + self.nl

        # template = MurphiTemplates.f_eq_msg_func
        # functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
        #                                                   []), 2) + self.nl

        # Queue Comparison
        functions += self.tab + "----" + __name__.replace('.','/') +  " : QueueComparisonFunctions" + self.nl

        template = MurphiTemplates.f_eq_same_ob
        functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                          ["sameInputOB", self.gen_ob_comp(MurphiTemplates.f_eq_queue_equal, MurphiTemplates.f_eq_queue_equal, systemStateAssoc, config, with_output=False)]), 2) + self.nl
        functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                          ["sameOutputOB", self.gen_ob_comp(MurphiTemplates.f_eq_queue_equal, MurphiTemplates.f_eq_queue_equal, systemStateAssoc, config, with_input=False)]), 2) + self.nl
        
        functions += self.add_tabs( "function sameOB(): boolean" + self.end + "begin" + self.nl \
                        + "  return sameInputOB() & sameOutputOB()" + self.end + "end" + self.end + self.nl, 2)
        functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                          ["can_RHS_replicate_OB", 
                                                           self.gen_ob_comp(MurphiTemplates.f_eq_queue_in_fixable, MurphiTemplates.f_eq_queue_out_fixable, 
                                                                            systemStateAssoc, config)]), 2) + self.nl

        # functions += self.tab + "----" + __name__.replace('.','/') +  " : BackupFunctions" + self.nl
        # functions += self.gen_rhs_backup(machineTypes, config)

        # functions += self.tab + "----" + __name__.replace('.','/') +  " : ReplicationFunctions" + self.nl
        # functions += self.gen_repl(systemStateAssoc, config)

        functions += self.tab + "----" + __name__.replace('.','/') +  " : RHS Restrictions" + self.nl
        if "dir" in config.eq_rhs:
            fn_inner = ""
            for ch in OptimizationHelper.supported_nets:
                template = MurphiTemplates.f_eq_queue_no_msg_from
                elem = "m_" + config.eq_rhs
                if config.use_mrecords:
                    template = MurphiTemplates.f_eq_mr_queue_no_msg_from
                    elem = config.eq_rhs
                fn_inner += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                            [config.eq_rhs.split("_")[0], ch, elem, "systemRHS" ]), 2)
            functions += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_same_ob),
                                                          ["L1RHSDone", fn_inner]), 2) + self.nl
        
        functions += self.tab + "----" + __name__.replace('.','/') +  " : GlobalStateManagementFunctions" + self.nl
        if not config.use_mrecords:
            template = MurphiTemplates.f_eq_global_state
            if config.eq_check_progress:
                template = MurphiTemplates.f_eqp_global_state
            functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                            ["& L1RHSDone()" if ("dir" in config.eq_rhs) else ""]), 2) + self.nl
        else:
            template = MurphiTemplates.f_eq_mr_global_state
            if config.eq_check_progress:
                template = MurphiTemplates.f_eqp_mr_global_state
            functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                            ["& L1RHSDone()" if ("dir" in config.eq_rhs) else ""]), 2) + self.nl

        if config.use_mrecords and config.eq_check and "cacheL1RHS" in machineTypes:
            functions += self.tab + "----" + __name__.replace('.','/') +  " : ActiveRHSFunction" + self.nl
            functions += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_mr_rhs_l1_only_one_active),
                                                                ["cacheL1RHS", "i_cacheL1RHS[n].cb[adr].State", "cacheL1RHS_I"]), 2) + self.nl


        murphi_str.append(functions)

    def gen_ob_comp(self, template_in: str, template_out: str, assoc: Dict[str, str], config: BaseConfig, with_input = True, with_output = True) -> str:
        obstr = ""

        # Check all input, i.e. the eq_LHS entity
        if with_input:
            obstr += "-- Inputs" + self.nl
            if config.use_mrecords:
                obstr += "alias elem : " + config.eq_lhs + " do" + self.nl
            else:
                obstr += "alias elem : from_m_" + config.eq_lhs.split("_")[0] + "(m_" + config.eq_lhs + ") do" + self.nl
            
            for ch in OptimizationHelper.supported_nets:
                if OptimizationHelper.has_arch_net(config.eq_lhs, ch, config) and OptimizationHelper.has_arch_net(config.eq_rhs, ch, config):
                    obstr += self.add_tabs(self._stringReplKeys(self._openTemplate(template_in),
                                                                [config.eq_lhs.split("_")[0], config.eq_rhs.split("_")[0], "systemLHSExt", "systemRHSExt", ch]), 1) + self.nl
                elif OptimizationHelper.has_arch_net(config.eq_lhs, ch, config):
                    obstr += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_no_msg_from),
                                                            [config.eq_lhs.split("_")[0], ch, "m_" + config.eq_lhs, "systemLHSExt"]), 1) + self.nl
                    
            obstr += "endalias" + self.end + self.nl

        # Check each output, i.e. the LHS_Ext
        if with_output:
            obstr += "-- Outputs" + self.nl
            for elem in assoc["systemLHSExt"]:
                if config.use_mrecords:
                    obstr += "for elem : OBJSET_" + EqCheckHelper.get_type(elem) + " do" + self.nl
                else:
                    obstr += "alias elem : from_m_" + elem.split("_")[0] + "(m_" + elem + ") do" + self.nl
            
                for ch in OptimizationHelper.supported_nets:
                    if OptimizationHelper.has_arch_net(elem, ch, config):
                        obstr += self.add_tabs(self._stringReplKeys(self._openTemplate(template_out),
                                                                    [elem.split("_")[0], elem.split("_")[0].replace("LHS", "RHS"), "systemLHS", "systemRHS", ch]), 1) + self.nl

                if config.use_mrecords:
                    obstr += "endfor" + self.end + self.nl
                else:
                    obstr += "endalias" + self.end + self.nl
            
        return self.add_tabs(obstr, 1)

    def gen_repl(self, assoc: Dict[str, str], config: BaseConfig) -> str:
        restr = ""
        

        # Check all input, i.e. the eq_LHS entity
        restr += "-- Inputs" + self.nl
        restr += "alias elem : from_m_" + config.eq_lhs.split("_")[0] + "(m_" + config.eq_lhs + ") do" + self.nl
        
        for ch in OptimizationHelper.supported_nets:
            if OptimizationHelper.has_arch_net(config.eq_lhs, ch, config) and OptimizationHelper.has_arch_net(config.eq_rhs, ch, config):
                restr += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_send_missing),
                                                            [config.eq_lhs.split("_")[0], config.eq_rhs.split("_")[0], "systemLHSExt", "systemRHSExt", ch]), 1) + self.nl

        restr += "endalias" + self.end + self.nl

        # Check each output, i.e. the LHS_Ext
        restr += "-- Outputs" + self.nl
        for elem in assoc["systemLHSExt"]:
            restr += "alias elem : from_m_" + elem.split("_")[0] + "(m_" + elem + ") do" + self.nl
            restr += "alias elem_rhs : map_" + elem.split("_")[0] + "_to_" + elem.split("_")[0].replace("LHS", "RHS") + "(elem) do" + self.nl
        
            for ch in OptimizationHelper.supported_nets:
                if OptimizationHelper.has_arch_net(elem, ch, config):
                    restr += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_copy),
                                                                [elem.split("_")[0], elem.split("_")[0].replace("LHS", "RHS"), "elem", "elem_rhs", ch, "map_LHS_msg_to_RHS"]), 1) + self.nl

            restr += "endalias" + self.end + self.nl
            restr += "endalias" + self.end + self.nl
        
        return self.add_tabs("procedure ReplicateRHS()" + self.end + "var lhs_offset: 0..O_NET_MAX" + self.end + "var rhs_offset: 0..O_NET_MAX" + self.end + "begin" + self.nl + self.add_tabs(restr, 1) + "end" + self.end, 1)