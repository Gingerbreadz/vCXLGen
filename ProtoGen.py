#  Copyright (c) 2022.  Nicolai Oswald
#  Copyright (c) 2022.  University of Edinburgh
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
#
#


from Protocols.MOESI_Directory.RF_Dir.ord_net.Run_Ord_RF import OrderedReplyForwardingProtocols

#gem5unorderedprotocols().run_protocol_tests()

## Snooping protocols
#SnoopingProtocolTest()                  # Make sure Murphi is correctly configured

#OrderedCHI()

## Reply forwarding protocols
OrderedReplyForwardingProtocols().run_protocol_tests()
#OrUnOrderedReplyForwardingProtocols.run_protocol_tests()
#UnorderedReplyForwardingProtocols()

## Intervention forwarding protocols
#OrderedInterventionForwardingProtocols().run_protocol_tests()

## Strict response forwarding
#OrderedStrictResponseProtocols()


#ReplicationProtocols().run_protocol_tests()

#run_next("MESI_SSP.pcc", path + reply_fwd_dir)

# FANCY STUFF
#run_next("Tardis.pcc", path)
# TSO-CC
#run_next("TSO_CC_MSI.pcc", path + reply_fwd_dir)
#run_next("TSO_CC_MESI.pcc", path + reply_fwd_dir)

# Feature test ord_unordered_net
feature_reply_fwd_dir = "RF_Dir/ord_unord_net/Feature_Tests/"
#run_next("MSI_no_I_store.pcc", path + feature_reply_fwd_dir)           # Auto completion for I store missing works
#run_next("MSI_manual_concurrency.pcc", path + feature_reply_fwd_dir)   # Manual concurrency added works
#run_next("MESI_j.pcc", path + feature_reply_fwd_dir)                   # Works too

# Unordered protocols
#run_next("MESI_unordered.pcc", path)


# Feature tests
#run_next("MSI_RF_Feature.pcc", path)
#run_next("MSI_RF_ProtoTest.pcc", path)
#run_next("MI_RF_extra_Ack.pcc", path)


print("ProtoGen complete")


