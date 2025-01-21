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

from Backend.Murphi.MurphiModular.MurphiTokens import MurphiTokens
from Backend.Common.TemplateHandler.TemplateHandler import TemplateHandler
from Backend.Murphi.MurphiTemp.TemplateHandler.MurphiTemplates import MurphiTemplates
from Backend.Murphi.BaseConfig import BaseConfig
from DataObjects.ClassCluster import Cluster


class GenInvariant(MurphiTokens, TemplateHandler):

    def __init__(self, murphi_str: List[str], clusters: List[Cluster], config: BaseConfig):
        TemplateHandler.__init__(self)

        if config.eq_check:
            murphi_str.append("--" + __name__.replace('.','/') + " : EqCheckLiveness" + self.nl + self.add_tabs(self.gen_eq_check_invariants(), 1))
        if config.eq_check_progress:
            murphi_str.append('liveness "can always track progress" g_system_state = systemRHS & g_progress_tracking;')
        if config.access_based_liveness:
            archs = set()
            for cluster in clusters:
                for arch in cluster.get_machine_architectures():
                    if str(arch) not in archs and "L1" in str(arch) and "cache" in str(arch):
                        archs.add(str(arch))
                        mach_count = cluster.get_machine_architecture_count(arch)
                        for i in range(mach_count):
                            murphi_str.append(self.gen_access_based_liveness(str(arch) + "_" + str(i)))

        murphi_str.append("--" + __name__.replace('.','/') + self.nl + self.add_tabs(self.gen_SWMR_invariant(config), 1))

    def gen_SWMR_invariant(self, config: BaseConfig):
        invstr = ""
        if not config.litmus_testing:
            if config.check_exclusive_write:
                invstr += self.gen_invariant_SW()
            if config.check_write_linearization:
                invstr += self.gen_invariant_EW()

        return invstr

    def gen_invariant_SW(self):
        return self._stringReplKeys(self._openTemplate(MurphiTemplates.f_invariant_SW),
                                    [self.k_address, self.k_machines, "store"]) + self.nl

    def gen_invariant_EW(self):
        return self._stringReplKeys(self._openTemplate(MurphiTemplates.f_invariant_EW),
                                    [self.k_address, self.k_machines, "store", "load"]) + self.nl

    def gen_eq_check_invariants(self):
        return self._stringReplKeys(self._openTemplate(MurphiTemplates.f_eq_check_invariant),
                                    []) + self.nl

    def gen_access_based_liveness(self, elem: str):
        return self._stringReplKeys(self._openTemplate(MurphiTemplates.f_access_based_liveness),
                                    [elem]) + self.nl
