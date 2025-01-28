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

from Backend.Murphi.BaseConfig import BaseConfig
from Backend.Murphi.MurphiModular.MurphiTokens import MurphiTokens
from Backend.Common.TemplateHandler.TemplateHandler import TemplateHandler
from Backend.Murphi.MurphiTemp.TemplateHandler.MurphiTemplates import MurphiTemplates

from DataObjects.ClassCluster import Cluster
from Debug.Monitor.ClassDebug import Debug


class GenPermFunc(TemplateHandler, Debug):

    def __init__(self, murphi_str: List[str], clusters: List[Cluster], config: BaseConfig):
        TemplateHandler.__init__(self)
        Debug.__init__(self)

        access_type = "----" + __name__.replace('.','/') + self.nl

        if not config.use_mrecords:
            template = MurphiTemplates.f_perm_func if not config.substitute_multisets else MurphiTemplates.f_perm_func_arr
            access_type += self.add_tabs(self._stringReplKeys(self._openTemplate(template),
                                                            [MurphiTokens.k_perm_type,
                                                            MurphiTokens.k_address,
                                                            MurphiTokens.k_machines]), 1) + self.nl
        else:
            clear_str = ""
            set_str = ""
            reset_str = ""

            archs = set([str(arch) for cluster in clusters for arch in cluster.get_machine_architectures()])
            for arch in archs:
                if "cache" in arch:
                    clear_str += "if !isundefined(m."+arch+") then" + self.nl
                    clear_str += self.tab + "g_perm." + arch + "[m."+arch+"][adr][acc] := false" + self.end
                    clear_str += "endif" + self.end

                    set_str += "if !isundefined(m."+arch+") then" + self.nl
                    set_str += self.tab + "g_perm." + arch + "[m."+arch+"][adr][acc] := true" + self.end
                    set_str += "endif" + self.end

                    reset_str += "for o : " + MurphiTokens.k_obj_set + arch + " do" + self.nl
                    reset_str += self.tab + "g_perm." + arch + "[o][adr][acc] := false" + self.end
                    reset_str += "endfor" + self.end

                    
            access_type += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_perm_func_mrecord),
                                                            [MurphiTokens.k_perm_type,
                                                            MurphiTokens.k_address,
                                                            MurphiTokens.k_machines,
                                                            self.add_tabs(clear_str, 2),
                                                            self.add_tabs(set_str, 1),
                                                            self.add_tabs(reset_str, 3),
                                                            ]), 1) + self.nl
            
            if config.access_based_liveness:
                archs = set()
                for cluster in clusters:
                    for arch in cluster.get_machine_architectures():
                        if str(arch) not in archs and "L1" in str(arch) and "cache" in str(arch) and cluster.get_machine_architecture_count(arch) > 1:
                            archs.add(str(arch))
    
                            access_type += self.add_tabs(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_mr_liveness_func),
                                                            [str(arch)]), 1) + self.nl    

        murphi_str.append(access_type)
