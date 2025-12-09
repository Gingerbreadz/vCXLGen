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

from typing import List, Set, Tuple

from Backend.Murphi.MurphiModular.OptimizationHelper import OptimizationHelper
from DataObjects.ClassCluster import Cluster
from DataObjects.ClassMultiDict import MultiDict

from Backend.Murphi.MurphiModular.MurphiTokens import MurphiTokens
from Backend.Common.TemplateHandler.TemplateHandler import TemplateHandler
from Backend.Murphi.MurphiTemp.TemplateHandler.MurphiTemplates import MurphiTemplates
from Backend.Murphi.BaseConfig import BaseConfig

from DataObjects.FlowDataTypes.ClassBaseAccess import BaseAccess
from Parser.NetworkxParser.ClassProtoParserBase import ProtoParserBase
from Parser.DataTypes.ClassBaseNetwork import Channel

from Backend.Murphi.MurphiModular.General.GenPCCToMurphi import GenPCCToMurphi

from Debug.Monitor.ClassDebug import Debug


class GenNetworkFunc(TemplateHandler, Debug):

    def __init__(self, murphi_str: List[str], clusters: List[Cluster], config: BaseConfig):
        TemplateHandler.__init__(self)
        Debug.__init__(self)

        network_str = ""

        network_str += self.gen_ordered_send_func(clusters, config)
        network_str += self.gen_unordered_send_func(clusters, config)

        # Generate Multicast functions if they exist
        network_str += self.gen_multicast_func(clusters, config)

        # Generate Broadcast functions if they exist
        network_str += self.gen_broadcast_func(clusters)

        # Generate the network ready check functions
        network_str += self.gen_network_ready_func(clusters, config)

        if config.prefetch_count > 0 or config.eq_check:
            used_str =  self.gen_network_ready_func(clusters, config).replace("ready", "used").replace("(" + MurphiTokens.c_ordered_const + "-" + str(config.total_mach_cnt) + ")", "1").replace("(" + MurphiTokens.c_unordered_const + "-" + str(config.total_mach_cnt) + ")", "1")
            used_str = used_str.replace("true;", "false ;").replace("false;", "true ;").replace("if !", "if ")
            network_str += used_str
            
        # Generate the network reset functions
        network_str += self.gen_network_reset(clusters, config)

        murphi_str.append("----" + __name__.replace('.','/') + self.nl + self.add_tabs(network_str, 1) + self.nl)

    def gen_ordered_send_func(self, clusters: List[Cluster], config: BaseConfig):
        network_str = ""
        if not config.use_per_machine_queues:
            network_functions = set()
            for global_arch in Cluster.get_global_architectures_in_clusters(clusters):

                # Total order network or point to point ordered network
                ord_net_func = MurphiTemplates.f_total_ordered_network_func
                if not config.enable_total_order_network:
                    ord_net_func = MurphiTemplates.f_ordered_network_func

                for ordered_network in global_arch.network.ordered_networks:
                    network_func = self._stringReplKeys(self._openTemplate(ord_net_func),
                                                        [str(ordered_network),
                                                        MurphiTokens.k_vector_cnt,
                                                        MurphiTokens.c_ordered_const,
                                                        MurphiTokens.k_machines])
                    if network_func not in network_functions:
                        network_functions.add(network_func)
                        network_str += network_func + self.nl + self.nl
        else:
            if not config.enable_total_order_network:
                self.perror("Per machine queues are only implemented for total ordered networks")
            nets = set()
            for cluster in clusters:
                for global_arch in cluster.get_global_architectures():
                    for net in global_arch.network.ordered_networks:
                        nets.add(net)
            for net in nets:
                send_body_str = ""
                pop_body_str = ""
                archs = set()
                for cluster in clusters:
                    for arch in cluster.get_machine_architectures():
                        if str(arch) in archs:
                            continue
                        archs.add(str(arch))

                        if not config.use_mrecords:
                            check = "Ismember(dst,OBJSET_"+str(arch)+")"
                            element = "dst"
                            if config.substitute_unions:
                                check = "isElement_"+str(arch)+"(dst)"
                                element = "from_m_"+str(arch)+"(dst)"

                            if OptimizationHelper.has_arch_net(str(arch), str(net), config):
                                send_body_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_network_func_send), [str(net), str(arch), check, element])
                                pop_body_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_network_func_pop), [str(net), str(arch), check, element])
                            else:
                                send_body_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_network_func_send_missing), [str(net), str(arch), check, element])
                                pop_body_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_network_func_pop_missing), [str(net), str(arch), check, element])
                        else:
                            if OptimizationHelper.has_arch_net(str(arch), str(net), config):
                                send_body_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_mr_func_send), [str(net), str(arch)])
                                pop_body_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_mr_func_pop), [str(net), str(arch)])
                            else:
                                send_body_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_mr_func_send_missing), [str(net), str(arch)])
                                pop_body_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_mr_func_pop_missing), [str(net), str(arch)])
                           

                send_end_body_str = ""
                pop_end_body_str = ""
                if config.eq_check:
                    send_end_body_str += "if is_machine_in_state(src, systemLHSExt) then" + self.nl
                    send_end_body_str += self.tab + self.tab + "Send_" + str(net) + "(map_LHS_msg_to_RHS(msg), map_LHS_to_RHS(src))" + self.end
                    send_end_body_str += self.tab + self.tab + "BackupRHS()" + self.end
                    send_end_body_str += self.tab + "endif" + self.end
                    pop_end_body_str += "if is_machine_in_state(dst, systemLHSExt) then" + self.nl
                    pop_end_body_str += self.tab + self.tab + "Pop_" + str(net) + "(map_LHS_to_RHS(dst), map_LHS_to_RHS(src))" + self.end
                    pop_end_body_str += self.tab + self.tab + "BackupRHS()" + self.end
                    pop_end_body_str += self.tab + "endif" + self.end

                    

                network_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_network_func),
                                                            [str(net),
                                                            MurphiTokens.k_machines,
                                                            send_body_str,
                                                            pop_body_str,
                                                            send_end_body_str,
                                                            pop_end_body_str]) \
                                    + self.nl + self.nl

        return network_str

    def gen_unordered_send_func(self, clusters: List[Cluster], config: BaseConfig) -> str:
        network_str = ""
        nets = set()
        if not config.use_per_machine_queues:
            for global_arch in Cluster.get_global_architectures_in_clusters(clusters):
                    for unordered_network in global_arch.network.unordered_networks:
                        if str(unordered_network) in nets:
                            continue
                        nets.add(str(unordered_network))
                        network_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_unordered_network_func),
                                                            [str(unordered_network),
                                                            MurphiTokens.c_unordered_const,
                                                            MurphiTokens.k_machines]) \
                                    + self.nl + self.nl
        else:
            if not config.enable_total_order_network:
                self.perror("Per machine queues are only implemented for total ordered networks")
            nets = set()
            for cluster in clusters:
                for global_arch in cluster.get_global_architectures():
                    for net in global_arch.network.unordered_networks:
                        nets.add(net)
            for net in nets:
                send_body_str = ""
                archs = set()
                for cluster in clusters:
                    for arch in cluster.get_machine_architectures():
                        if str(arch) in archs:
                            continue
                        archs.add(str(arch))

                        if config.use_mrecords:
                            self.perror("mrecords not supported for unordered networks")
                        else:

                            send_body_str += f"if Ismember(dst,OBJSET_{str(arch)}) then" +self.nl
                            if OptimizationHelper.has_arch_net(str(arch), str(net), config):
                                send_body_str += self.tab + self.tab + f"Assert (MultiSetCount(i:{str(net)}_{str(arch)}[dst], true) < U_NET_MAX) \"Too many messages to {str(arch)} {str(net)}\"" +self.end
                                send_body_str += self.tab + self.tab + f"MultiSetAdd(msg, {str(net)}_{str(arch)}[dst])" +self.end
                            else:
                                send_body_str += self.tab + self.tab + f"error \"invalid optimiztaion: removed {str(net)}_{str(arch)}\";" + self.end
                            send_body_str += self.tab + f"els"

                network_str += f"procedure Send_{str(net)}(msg:Message; src: Machines;)" + self.end
                network_str += "begin" + self.nl
                network_str += self.tab + "alias dst : msg.dst do" + self.nl
                network_str += self.tab + f"{send_body_str}e" + self.nl
                network_str += self.tab +  self.tab + "error \"unknown send machine\";" + self.nl
                network_str += self.tab + "endif;" + self.nl
                network_str += self.tab + "endalias;" + self.nl
                network_str += "end;" + self.nl + self.nl 
                
        return network_str

    ## Generate multicast functions
    # @param clusters A list of clusters which create the system
    def gen_multicast_func(self, clusters: List[Cluster], config: BaseConfig) -> str:
        multicast_str_list: List[str] = []
        multicast_str_list.append(self._multicast_gen_level(clusters, config))
        return ''.join(multicast_str_list)

    def _multicast_gen_level(self, clusters: List[Cluster], config: BaseConfig) -> str:
        multicast_str_list: List[str] = []

        archs = set()
        for arch in Cluster.get_machine_architectures_in_clusters(clusters):
            if config.eq_check:
                if str(arch).replace("RHS", "LHS") in archs:
                    continue
                archs.add(str(arch).replace("RHS", "LHS"))
            # Dict[variable_str, network_str]
            multi_cast_dict = MultiDict()

            transitions = arch.get_architecture_transitions()

            for transition in transitions:
                for operation in transition.operations:
                    children = operation.getChildren()
                    if str(operation) == ProtoParserBase.k_mcast:
                        self.perror("Message assigned to unknown network",
                                    str(children[0]) in arch.global_arch.network.unordered_networks or
                                    str(children[0]) in arch.global_arch.network.ordered_networks)
                        multi_cast_dict[str(children[0])] = str(children[2])

            self._multicast_func_gen(multicast_str_list, multi_cast_dict, clusters, config)

        return ''.join(multicast_str_list)

    def _multicast_func_gen(self, multicast_str_list: List[str], multi_cast_dict: MultiDict, clusters: List[Cluster], config: BaseConfig):
        for network_name in multi_cast_dict:
            var_defs = set(multi_cast_dict[network_name])
            for var_def in var_defs:
                if not config.use_mrecords:
                    template = MurphiTemplates.f_multicast_network_func
                    if config.substitute_multisets:
                        template = MurphiTemplates.f_multicast_network_func_arr
                    multicast_str_list.append(
                        self._stringReplKeys(self._openTemplate(template),
                                                                [network_name,
                                                                    GenPCCToMurphi().gen_vector(var_def),
                                                                    GenPCCToMurphi().gen_vector(var_def),
                                                                    MurphiTokens.k_machines])
                        + self.nl + self.nl)
                else:
                    body_str = ""
                    for arch in config.mrecords_vector[var_def]:
                        body_str += "for n : " + MurphiTokens.k_obj_set + arch + " do" + self.nl
                        body_str += self.tab + "if IsElement_" + var_def + "(dst_vect, to_m_" + arch + "(n)) then" + self.nl
                        body_str += self.tab + self.tab + "msg.dst := to_m_" + arch + "(n)" + self.end
                        body_str += self.tab + self.tab + "Send_" + network_name + "(msg, src)" + self.end
                        body_str += self.tab + "endif" + self.end
                        body_str += "endfor" + self.end
                    
                    multicast_str_list.append(
                        self._stringReplKeys(self._openTemplate(MurphiTemplates.f_multicast_network_func_mrecord),
                                                                [network_name,
                                                                    GenPCCToMurphi().gen_vector(var_def),
                                                                    GenPCCToMurphi().gen_vector(var_def),
                                                                    MurphiTokens.k_machines,
                                                                    self.add_tabs(body_str, 1)])
                        + self.nl + self.nl)

    ## Generate broadcast functions
    # @param A broadcast is only possible within the cluster
    def gen_broadcast_func(self, clusters: List[Cluster]) -> str:
        broadcast_str_list: List[str] = []
        for cluster in clusters:
            broadcast_str_list.append(self._broadcast_gen_cluster(cluster))
        # The broadcast must only happen in local cluster
        return "".join(broadcast_str_list)

    def _broadcast_gen_cluster(self, cluster: Cluster) -> str:
        broadcast_str_list: List[str] = []
        arch_set: Set[str] = set()
        # List of networks in cluster that are broadcasting
        broadcast_net_set: Set[str] = set()

        architectures = cluster.get_machine_architectures()
        for arch in architectures:
            transitions = arch.get_architecture_transitions()
            arch_set.add(str(arch))

            for transition in transitions:
                for operation in transition.operations:
                    children = operation.getChildren()
                    if str(operation) == ProtoParserBase.k_bcast:
                        self.perror("Message assigned to unknown network",
                                    str(children[0]) in arch.global_arch.network.unordered_networks or
                                    str(children[0]) in arch.global_arch.network.ordered_networks)
                        broadcast_net_set.add(str(children[0]))

        self._broadcast_func_gen(broadcast_str_list, broadcast_net_set, arch_set, cluster)
        return "".join(broadcast_str_list)

    # Broadcasts are limited to their cluster and cannot directly communicate across clusters
    def _broadcast_func_gen(self,
                            broadcast_str_list: List[str],
                            broadcast_net_set: Set[str],
                            arch_set: Set[str],
                            cluster: Cluster):
        cond_str = self._broadcast_func_cond_gen(arch_set)

        for network_name in broadcast_net_set:
            broadcast_str_list.append(self._stringReplKeys(self._openTemplate(MurphiTemplates.f_broadcast_network_func),
                                                           [network_name,
                                                            cluster.cluster_id,
                                                            cond_str,
                                                            MurphiTokens.k_machines])
                                      + self.nl + self.nl)

    ## Murphi cannot work with unions for IsMember functions, that is why it is necessary to test every set
    #
    def _broadcast_func_cond_gen(self, arch_set: Set[str]):
        arch_list = list(arch_set)
        cond_str = ""
        for ind in range(0, len(arch_list)):
            cond_str += "IsMember(dst, " + MurphiTokens.k_obj_set + arch_list[ind] + ")"
            if ind < len(arch_list)-1:
                cond_str += " | " + self.nl + self._broadcast_if_spacer()
        return cond_str

    def _broadcast_if_spacer(self) -> str:
        ret_tab = ""
        for ind in range(0, 7):
            ret_tab += self.tab
        return ret_tab

    ## Generate the network ready check function
    #
    def gen_network_ready_func(self, clusters: List[Cluster], config: BaseConfig) -> str:
        network_ready_str = ""

        request_networks, networks = self.filter_request_networks_by_channel(clusters)

        network_names: List[str] = []
        subtraction_cnt = config.total_mach_cnt
        # Substituted request network for network. All networks must be ready to serve a response to an issued request
        for network in networks:
            if str(network) in network_names:
                if (not config.eq_check):
                    Debug.pwarning("Multiple networks have same name and identifiers. This could potentially lead to "
                                   "deadlocks if this was not desired when designing the system")
                continue

            network_names.append(str(network))

            if network.vc_type == network.k_unordered and not config.use_per_machine_queues:
                network_ready_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_unordered_network_ready_func),
                                                          [str(network), MurphiTokens.c_unordered_const,
                                                           str(subtraction_cnt)]) + self.nl
            elif not config.use_per_machine_queues:
                # Total order network or point to point ordered network
                ord_net_func = MurphiTemplates.f_total_ordered_network_ready_func
                if not config.enable_total_order_network:
                    ord_net_func = MurphiTemplates.f_ordered_network_ready_func

                network_ready_str += self._stringReplKeys(self._openTemplate(ord_net_func),
                                                          [str(network), MurphiTokens.k_vector_cnt,
                                                           MurphiTokens.c_ordered_const, str(subtraction_cnt)]) \
                                     + self.nl
            elif config.eq_check:
                assert config.enable_total_order_network
                bodyLHS_str = ""
                bodyRHS_str = ""

                archs = set([str(arch) for cluster in clusters for arch in cluster.get_machine_architectures()])
                for arch in archs:
                    if OptimizationHelper.has_arch_net(arch, str(network), config):
                        body_str = "for dst:OBJSET_" + arch + " do" + self.nl + \
                            self.tab + "if cnt_" + str(network) + "_" + arch + "[dst] >= (" + MurphiTokens.c_ordered_const + "-" + str(subtraction_cnt) + ") then" + self.nl + \
                            self.tab + self.tab + "return false" + self.end + \
                            self.tab + "endif" + self.end + "endfor" + self.end
                        if "LHS" in arch:
                            bodyLHS_str += body_str
                        else:
                            bodyRHS_str += body_str
                    
                network_ready_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_network_ready),
                                                          [str(network) + "_LHS", self.add_tabs(bodyLHS_str, 1)])
                network_ready_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_network_ready),
                                                          [str(network) + "_RHS", self.add_tabs(bodyRHS_str, 1)])
            else:
                assert config.enable_total_order_network
                body_str = ""

                archs = set([str(arch) for cluster in clusters for arch in cluster.get_machine_architectures()])
                for arch in archs:
                    if OptimizationHelper.has_arch_net(arch, str(network), config):
                        body_str += "for dst:OBJSET_" + arch + " do" + self.nl
                        if network.vc_type == network.k_unordered:
                            body_str += self.tab + "if MultisetCount(i:" + str(network) + "_" + arch + "[dst], isundefined(" + str(network) + "_" + arch + "[dst][i].mtype)) >= (" + MurphiTokens.c_unordered_const + "-" + str(subtraction_cnt) + ") then" + self.nl
                        else:
                            body_str += self.tab + "if cnt_" + str(network) + "_" + arch + "[dst] >= (" + MurphiTokens.c_ordered_const + "-" + str(subtraction_cnt) + ") then" + self.nl
                        body_str += self.tab + self.tab + "return false" + self.end + \
                                    self.tab + "endif" + self.end + "endfor" + self.end
                
                network_ready_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_pmq_tot_o_network_ready),
                                                          [str(network), self.add_tabs(body_str, 1)]) \

        if config.eq_check:
            return network_ready_str + self.gen_global_check_network_ready_func(networks, "_LHS") + self.gen_global_check_network_ready_func(networks, "_RHS") + self.nl


        return network_ready_str + self.gen_global_check_network_ready_func(networks) + self.nl

    def gen_global_check_network_ready_func(self, networks: Set[Channel], side: str = ""):
        global_network_ready_inner = ""
        nets = set()
        for network in networks:
            if str(network) in nets:
                continue
            nets.add(str(network))
            global_network_ready_inner += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_network_ready_inner),
                                                               [str(network)+side]) + self.nl

        return self._stringReplKeys(self._openTemplate(MurphiTemplates.f_network_ready_outer),
                                    [global_network_ready_inner, side]) + self.nl

    @staticmethod
    def filter_request_networks_by_channel(clusters: List[Cluster]) -> Tuple[Set[Channel], Set[Channel]]:
        request_networks: Set[Channel] = set()
        networks: Set[Channel] = set()

        for cluster in clusters:
            for arch in cluster.get_machine_architectures():
                transitions = arch.get_architecture_transitions()

                for transition in transitions:
                    for out_msg in transition.out_msg:
                        networks.add(out_msg.base_msg.vc)
                        if isinstance(transition.guard, BaseAccess.Access_type):
                            request_networks.add(out_msg.base_msg.vc)

        return request_networks, networks

    def gen_network_reset(self, clusters: List[Cluster], config: BaseConfig) -> str:
        return self._stringReplKeys(self._openTemplate(MurphiTemplates.f_fifo_reset_body),
                                    [MurphiTokens.k_net, self.gen_network_reset_func(clusters, config)]) \
               + self.nl + self.nl

    def gen_network_reset_func(self, clusters: List[Cluster], config: BaseConfig) -> str:
        ordered_network_set = set()
        unordered_network_set = set()

        # Generate a list of all machines and networks
        for cluster in clusters:

            for global_arch in cluster.get_global_architectures():
                ordered_network_set.update(global_arch.network.ordered_networks.keys())
                unordered_network_set.update(global_arch.network.unordered_networks.keys())

        self.perror("Ordered and unordered networks have identical identifiers",
                    not ordered_network_set.intersection(unordered_network_set))

        if not config.use_per_machine_queues:
            return self.add_tabs(self.gen_ordered_network_reset_str(ordered_network_set, config)
                                + self.gen_unordered_network_reset_str(unordered_network_set), 1)
        else:
            assert config.enable_total_order_network
            body_str = ""

            archs = set([str(arch) for cluster in clusters for arch in cluster.get_machine_architectures()])
            for arch in archs:
                for network in ordered_network_set:
                    if OptimizationHelper.has_arch_net(arch, str(network), config):
                        body_str += "undefine " + str(network) + "_" + arch + self.end

                body_str += "for dst:OBJSET_" + arch + " do" + self.nl
                
                for network in ordered_network_set:
                    if OptimizationHelper.has_arch_net(arch, str(network), config):
                        body_str += self.tab + "cnt_" + str(network) + "_" + arch + "[dst] := 0" + self.end
                
                body_str += "endfor" + self.end + self.nl

            for arch in archs:
                for network in unordered_network_set:
                    if OptimizationHelper.has_arch_net(arch, str(network), config):
                        body_str += "undefine " + str(network) + "_" + arch + self.end
            # body_str += self.gen_unordered_network_reset_str(unordered_network_set)
                
            return self.add_tabs(body_str, 1)

    def gen_ordered_network_reset_str(self, ordered_network_list: Set[str], config: BaseConfig) -> str:
        ordered_network_reset_str = ""

        # Total order network or point to point ordered network
        ord_net_func = MurphiTemplates.f_total_ordered_reset
        if not config.enable_total_order_network:
            ord_net_func = MurphiTemplates.f_ordered_reset

        for ordered_network in ordered_network_list:
            ordered_network_reset_str += self._stringReplKeys(self._openTemplate(ord_net_func),
                                                              [str(ordered_network), MurphiTokens.k_vector_cnt]
                                                              ) + self.nl

        return ordered_network_reset_str

    def gen_unordered_network_reset_str(self, unordered_network_list: Set[str]) -> str:
        unordered_network_reset_str = ""

        for unordered_network in unordered_network_list:
            unordered_network_reset_str += self._stringReplKeys(self._openTemplate(MurphiTemplates.f_unordered_reset),
                                                                [str(unordered_network)]) + self.nl

        return unordered_network_reset_str
