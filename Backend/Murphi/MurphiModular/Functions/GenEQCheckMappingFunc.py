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


class GenEQCheckMappingFunc(TemplateHandler, Debug):

    def __init__(self, murphi_str: List[str], clusters: List[Cluster], config: BaseConfig):
        TemplateHandler.__init__(self)
        Debug.__init__(self)

        functions = "----" + __name__.replace('.','/') + self.nl
        
        if config.use_mrecords:
            functions += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_mr_mappings),
                                                            [self.gen_mappings(clusters, config), config.eq_lhs, config.eq_rhs]), 1) + self.nl
        else:
            functions += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_mappings),
                                                            [self.gen_mappings(clusters, config)]), 1) + self.nl
        

        template = MurphiTemplates.f_eq_x_mappings
        functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                        [config.eq_lhs.split("_")[0], config.eq_rhs.split("_")[0]]), 1) + self.nl
        archs = set()
        for cluster in clusters:
            for arch in cluster.get_machine_architectures():
                if str(arch) in archs:
                    continue
                archs.add(str(arch))

                if "L2" in str(arch) and "LHS" in str(arch):
                    lhs = str(arch)
                    rhs = str(arch).replace("LHS", "RHS")

                    functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                        [lhs, rhs]), 1) + self.nl

        functions += self.tab + "----" + __name__.replace('.','/') +  " : StateAssociation" + self.nl
        assoc = EqCheckHelper.get_state_assoc(EqCheckHelper.systemStates, EqCheckHelper.get_machines(clusters), config)
        template = MurphiTemplates.f_eq_global_state_association
        functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                          [self.gen_state_assoc(EqCheckHelper.systemStates, assoc, config)]), 1) + self.nl
        
        functions += self.tab + "----" + __name__.replace('.','/') +  " : MessageComparisonFunctions" + self.nl
        template = MurphiTemplates.f_eq_mr_msg_func if config.use_mrecords else MurphiTemplates.f_eq_msg_func
        functions += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                          []), 2) + self.nl

        functions += self.tab + "----" + __name__.replace('.','/') +  " : BackupFunctions" + self.nl
        functions += self.gen_rhs_backup(EqCheckHelper.get_machine_types(clusters), config)

        murphi_str.append(functions)
    
    
    def gen_state_assoc(self, systemStates: List[str], assoc: Dict[str, str], config: BaseConfig) -> str:
        assocs = ""
                
        for state in systemStates:
            assocs += "if s = " + state + " then" + self.nl

            for machine in assoc[state]:
                if config.use_mrecords:
                    assocs += self.tab + "if !isundefined(m." + EqCheckHelper.get_type(machine) + ") then" + self.nl    
                else:
                    assocs += self.tab + "if m = m_" + machine + " then" + self.nl
                assocs += self.tab + self.tab + "return true" + self.end
                assocs += self.tab + "endif" + self.end

            assocs += self.tab + "return false" + self.end
            assocs += "endif" + self.end

        return self.add_tabs(assocs, 1)

    def gen_rhs_backup(self, machineTypes: List[str], config: BaseConfig) -> str:
        bkstr = ""
        channels = ["req", "resp", "fwd"]

        bkstr += "procedure BackupRHS()" + self.end
        bkstr += "begin" + self.nl
        for machine in machineTypes:
            if "RHS" in machine:
                bkstr += self.tab + "for elem : OBJSET_" + machine + " do " + self.nl
                bkstr += self.tab + self.tab + "i_"+machine+"_BKUP[elem] := i_"+ machine + "[elem]" + self.end + self.nl
                
                for ch in channels:
                    if OptimizationHelper.has_arch_net(machine, ch, config):
                        bkstr += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_copy),
                                                                [machine, machine+"_BKUP", "elem", "elem", ch, ""]), 2) + self.nl

                bkstr += self.tab + "endfor" + self.end
        bkstr += "end" + self.end + self.nl

        bkstr += "procedure RestoreRHSBackup()" + self.end
        bkstr += "begin" + self.nl
        for machine in machineTypes:
            if "RHS" in machine:
                bkstr += self.tab + "for elem : OBJSET_" + machine + " do " + self.nl
                bkstr += self.tab + self.tab + "i_"+machine+"[elem] := i_"+ machine + "_BKUP[elem]" + self.end + self.nl
                
                for ch in channels:
                    if OptimizationHelper.has_arch_net(machine, ch, config):
                        bkstr += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_queue_copy),
                                                                [machine+"_BKUP", machine, "elem", "elem", ch, ""]), 2) + self.nl

                bkstr += self.tab + "endfor" + self.end
        bkstr += "end" + self.end + self.nl

        return self.add_tabs(bkstr, 2)

    def gen_mappings(self, clusters: List[Cluster], config: BaseConfig) -> str:
        map_s = ""

        assoc = EqCheckHelper.get_state_assoc(EqCheckHelper.systemStates, EqCheckHelper.get_machines(clusters), config)

        if not config.use_mrecords:
            map_s += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_mappings_inner),
                                                            [config.eq_lhs, config.eq_rhs]), 1)

        for elem in assoc["systemLHSExt"]:
            template = MurphiTemplates.f_eq_mappings_inner 
            if config.use_mrecords:
                template = MurphiTemplates.f_eq_mr_mappings_inner
                elem = EqCheckHelper.get_type(elem)
            map_s += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                        [elem, elem.replace("LHS", "RHS")]), 1)

        return map_s
    
