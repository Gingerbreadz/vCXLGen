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
from Debug.Monitor.ClassDebug import Debug


class GenVectorFunc(TemplateHandler, Debug):

    def __init__(self, murphi_str: List[str], config: BaseConfig):
        TemplateHandler.__init__(self)
        Debug.__init__(self)

        vector_func_str = ""

        if config.var_vector_map:
            for vector in config.var_vector_map:
                if not config.use_mrecords:
                    template = MurphiTemplates.f_vector_func if not config.substitute_multisets else MurphiTemplates.f_vector_func_arr
                    vector_func_str += (self._stringReplKeys(self._openTemplate(template),
                                                            [vector,
                                                            MurphiTokens.k_vector + vector,
                                                            MurphiTokens.k_machines,
                                                            MurphiTokens.k_vector_cnt]) +
                                        self.nl + self.nl)
                else:
                    add_body = ""
                    remove_body = ""
                    clear_body = ""
                    element_body = ""
                    count_body = ""

                    for arch in config.mrecords_vector[vector]:
                        add_body += "if !isundefined(n."+arch+") then" + self.nl + self.tab + "sv." + arch + "[n."+arch+"] := true" + self.end + "endif" + self.end
                        remove_body += "if !isundefined(n."+arch+") then" + self.nl + self.tab + "sv." + arch + "[n."+arch+"] := false" + self.end + "endif" + self.end
                        clear_body += "for m : "+MurphiTokens.k_obj_set+arch+" do" + self.nl + self.tab + "sv." + arch + "[m] := false" + self.end + "endfor" + self.end
                        element_body += "if !isundefined(n."+arch+") then" + self.nl + self.tab + "return sv." + arch + "[n."+arch+"]" + self.end + "endif" + self.end
                        count_body += "for m : "+MurphiTokens.k_obj_set+arch+" do" + self.nl + self.tab + "if sv." + arch + "[m] then" + self.nl + self.tab + self.tab + "cnt := cnt + 1" + self.end + self.tab + "endif" + self.end + "endfor" + self.end
                
                    
                    vector_func_str += (self._stringReplKeys(self._openTemplate(MurphiTemplates.f_vector_func_mrecord),
                                                            [vector,
                                                            MurphiTokens.k_vector + vector,
                                                            MurphiTokens.k_machines,
                                                            MurphiTokens.k_vector_cnt,
                                                            self.add_tabs(add_body, 1),
                                                            self.add_tabs(remove_body, 1),
                                                            self.add_tabs(clear_body, 1),
                                                            self.add_tabs(element_body, 1),
                                                            self.add_tabs(count_body, 1)]) +
                                        self.nl + self.nl)

            murphi_str.append("----" + __name__.replace('.','/') + self.nl + self.add_tabs(vector_func_str, 1))

