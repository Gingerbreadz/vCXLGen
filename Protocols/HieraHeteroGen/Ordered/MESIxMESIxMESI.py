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

import pathlib
from Algorithms.HeteroGen.RunTestFullSystem import RunFullSystem
import MurphiLitmusTests.LitmusTests.SC.GenLitmusTests
import MurphiLitmusTests.LitmusTests.RC.GenLitmusTests

from Protocols.MOESI_Directory.RF_Dir.ord_net.Run_Ord_RF import OrderedReplyForwardingProtocols
from Debug.Monitor.ClassDebug import Debug


# Ordered reply forwarding communication pattern protocols
class MESIxMESIxMESI(RunFullSystem, Debug):

    translation_table_first = {'load': ['load'], 'store': ['store']} # MESI
    translation_table_second = {'load': ['load'], 'store': ['store']} # MESI
    translation_table_third = {'load': ['load'], 'store': ['store']} # MESI

    def __init__(self, eq_checks = False):
        RunFullSystem.__init__(self)
        Debug.__init__(self, True)
        self.sc_litmus_test_gen = MurphiLitmusTests.LitmusTests.SC.GenLitmusTests.GenLitmusTests()
        self.rc_litmus_test_gen = MurphiLitmusTests.LitmusTests.RC.GenLitmusTests.GenLitmusTests()

        self.run_protocol_tests(eq_checks)

    def run_protocol_tests(self, eq_checks = False):
        path = OrderedReplyForwardingProtocols().get_cur_protocol_path()
        protocol_1_name: str = "MESI.pcc"
        protocol_2_name: str = "MESI.pcc"
        protocol_3_name: str = "MESI.pcc"
        self.run_test(protocol_1_name, protocol_2_name, protocol_3_name, path,
                      [self.translation_table_first, self.translation_table_second], [self.translation_table_third, self.translation_table_second],
                      self.sc_litmus_test_gen.litmus_test_list, self.rc_litmus_test_gen.litmus_test_list, eq_checks=eq_checks)
        self.psuccess(f"HieraHeteroGen {protocol_1_name.split('.')[0]} x {protocol_2_name.split('.')[0]} x {protocol_3_name.split('.')[0]} execution complete")

    @staticmethod
    def get_cur_protocol_path():
        return pathlib.Path(__file__).parent.absolute()
