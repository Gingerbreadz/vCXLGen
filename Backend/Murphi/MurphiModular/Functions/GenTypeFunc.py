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

from typing import List

from Backend.Common.TemplateHandler.TemplateHandler import TemplateHandler
from Backend.Murphi.MurphiTemp.TemplateHandler.MurphiTemplates import MurphiTemplates
from Backend.Murphi.MurphiModular.MurphiTokens import MurphiTokens
from Backend.Murphi.BaseConfig import BaseConfig
from DataObjects.ClassCluster import Cluster
from Debug.Monitor.ClassDebug import Debug


class GenTypeFunc(TemplateHandler, Debug):

    def __init__(self, murphi_str: List[str], clusters: List[Cluster], config: BaseConfig):
        TemplateHandler.__init__(self)
        Debug.__init__(self)

        type_func_str = ""

        if config.substitute_unions or config.use_mrecords:
            archs = set()
            for cluster in clusters:
                for arch in cluster.get_machine_architectures():
                    if str(arch) in archs:
                        continue
                    archs.add(str(arch))

                    if config.substitute_unions:
                        # Create isElement Functions
                        type_str = ""
                        for idx in range(cluster.get_machine_architecture_count(arch)):
                            if idx > 0:
                                type_str += " | "
                            type_str += "m = " + MurphiTokens.k_m_set + str(arch) + "_" + str(idx)
                            
                        type_func_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_is_element),
                                        [
                                            str(arch),
                                            type_str
                                        ]) + self.nl + self.nl
                        
                    # Create instance to machine mappings
                    to_m_str = ""
                    from_m_str = ""
                    to_vars_str = ""

                    if config.substitute_unions:
                        if cluster.get_machine_architecture_count(arch) > 1: 
                            # Handling of scalarsets
                            to_m_str += "return i_" + MurphiTokens.k_sm + str(arch) + "[o]" + self.end

                            from_m_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_scalar_m_mapping_for),
                                        [
                                            str(arch),
                                            MurphiTokens.k_obj_set,
                                            MurphiTokens.k_sm
                                        ])
                        else:
                            # Currently idx will only ever be 0, as other cases are all handled as scalarsets, this accounts for the if condition above might changing in the future
                            if cluster.get_machine_architecture_count(arch) > 1:
                                for idx in range(cluster.get_machine_architecture_count(arch)):
                                    to_m_str += "if o =     " + str(arch) + "_" + str(idx) + " then" + self.nl + \
                                        self.tab + "return " + MurphiTokens.k_m_set + str(arch) + "_" + str(idx) + self.end + "els"
                                to_m_str += "e" + self.nl + self.tab + "error \"can not map to m_" + str(arch) + "\"" + self.nl + "endif" + self.end

                                for idx in range(cluster.get_machine_architecture_count(arch)):
                                    from_m_str += "if m = " + MurphiTokens.k_m_set + str(arch) + "_" + str(idx) + " then" + self.nl + \
                                        self.tab + "return " + str(arch) + "_" + str(idx) + self.end + "els"
                                from_m_str += "e" + self.nl + self.tab + "error \"can not map from m_" + str(arch) + "\"" + self.nl + "endif" + self.end
                            else:
                                to_m_str += "if o =     " + str(arch) + " then" + self.nl + \
                                        self.tab + "return " + MurphiTokens.k_m_set + str(arch) + "_" + str(idx) + self.end + "els"
                                to_m_str += "e" + self.nl + self.tab + "error \"can not map to m_" + str(arch) + "\"" + self.nl + "endif" + self.end

                                from_m_str += "if m = " + MurphiTokens.k_m_set + str(arch) + "_" + str(idx) + " then" + self.nl + \
                                        self.tab + "return " + str(arch) + self.end + "els"
                                from_m_str += "e" + self.nl + self.tab + "error \"can not map from m_" + str(arch) + "\"" + self.nl + "endif" + self.end
                    else:
                        to_vars_str = "var m: Machines;"
                        to_m_str = "undefine m" + self.end + "m." + str(arch) + " := o" + self.end + "return m" + self.end
                        from_m_str = "return m." + str(arch) + self.end        


                    type_func_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_m_mappings),
                                    [
                                        str(arch),
                                        MurphiTokens.k_obj_set,
                                        self.add_tabs(to_m_str, 1).rstrip("\n"),
                                        self.add_tabs(from_m_str, 1).rstrip("\n"),
                                        to_vars_str
                                    ]) + self.nl + self.nl

            murphi_str.append("----" + __name__.replace('.','/') + self.nl + self.add_tabs(type_func_str, 1))

