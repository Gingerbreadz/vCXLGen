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

from Backend.Murphi.MurphiModular.RumurHelper import RumurHelper
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
        machines = self.get_machines(clusters)
        machineTypes = self.get_machine_types(clusters)
        systemStateAssoc = self.get_state_assoc(systemStates, machines, config)

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
            for ch in ["req", "resp", "fwd"]:
                fn_inner += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_no_msg_from),
                                                            [config.eq_rhs.split("_")[0], ch, "m_" + config.eq_rhs, "systemRHS" ]), 2)
            functions += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_same_ob),
                                                          ["L1RHSDone", fn_inner]), 2) + self.nl
        
        functions += self.tab + "----" + __name__.replace('.','/') +  " : GlobalStateManagementFunctions" + self.nl
        template = MurphiTemplates.f_eqp_global_state if config.eq_check_progress else MurphiTemplates.f_eq_global_state
        functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                          ["& L1RHSDone()" if ("dir" in config.eq_rhs) else ""]), 2) + self.nl

        murphi_str.append(functions)
    
    def get_machine_types(self, clusters: List[Cluster]) -> List[str]:
        archs = set()
        for cluster in clusters:
            archs.update(set(machine.arch for machine in cluster.system_tuple))

        return list(set([ str(x) for x in list(archs)]))
    
    def get_machines(self, clusters: List[Cluster]) -> List[str]:
        archs = set()
        for cluster in clusters:
            for arch in cluster.get_machine_architectures():
                mach_count = cluster.get_machine_architecture_count(arch)
                for i in range(mach_count):
                    archs.add(str(arch) + "_" + str(i))

        return list(archs)

    def get_state_assoc(self, systemStates: List[str], machines: List[str], config: BaseConfig) -> Dict[str, str]:
        assoc = {}
        for state in systemStates:
            assoc[state] = []

        for machine in machines:
            if machine == config.eq_lhs:
                assoc["systemLHS"].append(machine)
            elif machine == config.eq_rhs: 
                assoc["systemRHS"].append(machine)
            elif "L1" in machine:
                if "LHS" in machine:
                    assoc["systemLHS"].append(machine)
                elif "RHS" in machine:
                    assoc["systemRHS"].append(machine)
            elif "L2" in machine:
                if "LHS" in machine:
                    assoc["systemLHSExt"].append(machine)
                elif "RHS" in machine:
                    assoc["systemRHSExt"].append(machine)

        return assoc

    def gen_ob_comp(self, template_in: str, template_out: str, assoc: Dict[str, str], config: BaseConfig, with_input = True, with_output = True) -> str:
        obstr = ""
        channels = ["req", "resp", "fwd"]

        # Check all input, i.e. the eq_LHS entity
        if with_input:
            obstr += "-- Inputs" + self.nl
            obstr += "alias elem : from_m_" + config.eq_lhs.split("_")[0] + "(m_" + config.eq_lhs + ") do" + self.nl
            
            for ch in channels:
                if RumurHelper.has_arch_net(config.eq_lhs, ch, config) and RumurHelper.has_arch_net(config.eq_rhs, ch, config):
                    obstr += self.add_tabs(self._stringReplKeys(self._openTemplate(template_in),
                                                                [config.eq_lhs.split("_")[0], config.eq_rhs.split("_")[0], "systemLHSExt", "systemRHSExt", ch]), 1) + self.nl
                elif RumurHelper.has_arch_net(config.eq_lhs, ch, config):
                    obstr += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_no_msg_from),
                                                            [config.eq_lhs.split("_")[0], ch, "m_" + config.eq_lhs, "systemLHSExt"]), 1) + self.nl
                    
            obstr += "endalias" + self.end + self.nl

        # Check each output, i.e. the LHS_Ext
        if with_output:
            obstr += "-- Outputs" + self.nl
            for elem in assoc["systemLHSExt"]:
                obstr += "alias elem : from_m_" + elem.split("_")[0] + "(m_" + elem + ") do" + self.nl
            
                for ch in channels:
                    if RumurHelper.has_arch_net(elem, ch, config):
                        obstr += self.add_tabs(self._stringReplKeys(self._openTemplate(template_out),
                                                                    [elem.split("_")[0], elem.split("_")[0].replace("LHS", "RHS"), "systemLHS", "systemRHS", ch]), 1) + self.nl

                obstr += "endalias" + self.end + self.nl
            
        return self.add_tabs(obstr, 1)

    def gen_repl(self, assoc: Dict[str, str], config: BaseConfig) -> str:
        restr = ""
        channels = ["req", "resp", "fwd"]

        # Check all input, i.e. the eq_LHS entity
        restr += "-- Inputs" + self.nl
        restr += "alias elem : from_m_" + config.eq_lhs.split("_")[0] + "(m_" + config.eq_lhs + ") do" + self.nl
        
        for ch in channels:
            if RumurHelper.has_arch_net(config.eq_lhs, ch, config) and RumurHelper.has_arch_net(config.eq_rhs, ch, config):
                restr += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_send_missing),
                                                            [config.eq_lhs.split("_")[0], config.eq_rhs.split("_")[0], "systemLHSExt", "systemRHSExt", ch]), 1) + self.nl

        restr += "endalias" + self.end + self.nl

        # Check each output, i.e. the LHS_Ext
        restr += "-- Outputs" + self.nl
        for elem in assoc["systemLHSExt"]:
            restr += "alias elem : from_m_" + elem.split("_")[0] + "(m_" + elem + ") do" + self.nl
            restr += "alias elem_rhs : map_" + elem.split("_")[0] + "_to_" + elem.split("_")[0].replace("LHS", "RHS") + "(elem) do" + self.nl
        
            for ch in channels:
                if RumurHelper.has_arch_net(elem, ch, config):
                    restr += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_copy),
                                                                [elem.split("_")[0], elem.split("_")[0].replace("LHS", "RHS"), "elem", "elem_rhs", ch, "map_LHS_msg_to_RHS"]), 1) + self.nl

            restr += "endalias" + self.end + self.nl
            restr += "endalias" + self.end + self.nl
        
        return self.add_tabs("procedure ReplicateRHS()" + self.end + "var lhs_offset: 0..O_NET_MAX" + self.end + "var rhs_offset: 0..O_NET_MAX" + self.end + "begin" + self.nl + self.add_tabs(restr, 1) + "end" + self.end, 1)