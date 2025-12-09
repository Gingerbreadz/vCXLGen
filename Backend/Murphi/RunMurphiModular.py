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

import os
import copy
from psutil import virtual_memory

from typing import List, Union, Tuple

from time import sleep

from Backend.Murphi.BaseConfig import BaseConfig
from Backend.Murphi.ModularMurphi import ModularMurphi
from Debug.Monitor.ClassDebug import Debug
from Debug.Monitor.MakeDir import make_dir

from DataObjects.ClassCluster import Cluster
from MurphiLitmusTests.ClassLitmusTest import LitmusTest


def _run_murphi_modular_base(clusters: List[Cluster],
                             filename: str,
                             litmus_test: Union[LitmusTest, None] = None,
                             run_SSP: bool = False,
                             custom_dir: str = '',
                             config: dict = {},
                            #  eq_checks: bool = False,
                            #  full_sys: bool = False,
                            #  cc_num=2,
                            #  minimal=False,
                            #  prefetch_count=0,
                             ) -> Tuple[ModularMurphi, str]:
    def_path = os.getcwd()

    path = "Murphi/"
    if custom_dir:
        path += custom_dir + '/'
    if litmus_test:
        path += litmus_test.test_name.split('.')[0]
    make_dir(path)

    if not config.get("minimal", False) or not config.get("eq_checks", False):
        murphi_desc = ModularMurphi(clusters, "MU_" + filename, False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=config|{"use_per_machine_queues":True, "remove_unused_channels":True, "minimize_queue_size": True}))

    if not config.get("minimal", False):
        murphi_desc = ModularMurphi(clusters, filename, False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=config))

        # Rumur version that should be as similar to MURPHI as possible
        # ModularMurphi(clusters, "RMR_" + filename, False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.RumurDefault()|{"full_sys": full_sys}))

        ModularMurphi(clusters, "RMR_MR_" + filename, False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.RumurDefault()|config|{"use_mrecords": True, "substitute_unions": False}))

    if not config.get("eq_checks", False):
        if not config.get("minimal", False):
            # Rumur version for the compositional verification, with abstractions on L2 & access based litmus tests for each L1
            ModularMurphi(clusters, "RMR_LIVE_" + filename, False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.RumurDefault()|config|{"access_based_liveness":True}))
            ModularMurphi(clusters, "RMR_MR_LIVE_" + filename, False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.RumurDefault()|config|{"access_based_liveness":True, "use_mrecords": True, "substitute_unions": False}))

    else:
        # TODO: Find a better way to handle this
        config["eq_other_mi_downgrade"] = "RCC" in config["sys_list"]["C1"]
        config["eq_self_mi_downgrade"] = not config["eq_other_mi_downgrade"]

        cc_num = config.get("cc_num", 2)
        # Rumur version for the compositional verification, with abstractions on L2 & access based litmus tests for each L1
        # TODO: Reenable
        ModularMurphi(clusters, f"COMP_Model_{cc_num}CC", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.RumurDefault()|config|{"access_based_liveness":True, "use_mrecords": True, "substitute_unions": False}))
        # Directory subset Cache
        eq_lhs_clusters = []
        eq_rhs_clusters = []
        for cluster in clusters:
            systems = []
            names = set()
            for system in cluster.system_tuple:
                rhs_system = copy.deepcopy(system)
                rhs_system.arch.arch_name += "LHS"
                
                if rhs_system.arch.arch_name not in names:
                    systems.append(rhs_system)
                    if "cacheL1" in system.arch.arch_name:
                        for i in range(1, cc_num):
                            systems.append(rhs_system)
                    names.add(rhs_system.arch.arch_name)
            eq_lhs_clusters.append(Cluster(tuple(systems), cluster.cluster_id + '_LHS', False))

            if cluster.cluster_id == "C2":
                systems = []
                for system in cluster.system_tuple:
                    if not "L1" in system.arch.arch_name:
                        rhs_system = copy.deepcopy(system)
                        rhs_system.arch.arch_name += "RHS"

                        if rhs_system.arch.arch_name not in names:
                            systems.append(rhs_system)
                            names.add(rhs_system.arch.arch_name)
                            if "cacheL2" in system.arch.arch_name:
                                rhs_system = copy.deepcopy(system)
                                rhs_system.arch.arch_name = "abstractionRHS"
                                systems.append(rhs_system)
                                names.add(rhs_system.arch.arch_name)
                            
                eq_rhs_clusters.append(Cluster(tuple(systems), 'C2_RHS', False))

        if not config.get("minimal", False):
            ModularMurphi(eq_lhs_clusters + eq_rhs_clusters, f"COMP_MR_EQ_BsL2_{cc_num}CC", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.EqCheckMRDefault()|config|{"eq_check_progress":False}))
        
        murphi_desc = ModularMurphi(eq_lhs_clusters + eq_rhs_clusters, f"COMP_MR_EQP_BsL2_{cc_num}CC", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.EqCheckMRDefault()|config))
        
        eq_rhs_clusters = []
        eq_lhs_clusters = []
        for cluster in clusters:
            systems = []
            names = set()
            for system in cluster.system_tuple:
                lhs_system = copy.deepcopy(system)
                lhs_system.arch.arch_name += "RHS"
                
                if lhs_system.arch.arch_name not in names:
                    systems.append(lhs_system)
                    if "cacheL1" in system.arch.arch_name:
                        for i in range(1, cc_num):
                            systems.append(lhs_system)
                    names.add(lhs_system.arch.arch_name)
            eq_rhs_clusters.append(Cluster(tuple(systems), cluster.cluster_id + '_RHS', False))

            if cluster.cluster_id == "C2":
                systems = []
                for system in cluster.system_tuple:
                    if not "L1" in system.arch.arch_name:
                        lhs_system = copy.deepcopy(system)
                        lhs_system.arch.arch_name += "LHS"

                        if lhs_system.arch.arch_name not in names:
                            systems.append(lhs_system)
                            names.add(lhs_system.arch.arch_name)
                            if "cacheL2" in system.arch.arch_name:
                                lhs_system = copy.deepcopy(system)
                                lhs_system.arch.arch_name = "abstractionLHS"
                                systems.append(lhs_system)
                                names.add(lhs_system.arch.arch_name)
                            
                eq_lhs_clusters.append(Cluster(tuple(systems), 'C2_LHS', False))
        
        ModularMurphi(eq_rhs_clusters + eq_lhs_clusters, f"COMP_MR_EQ_L2sB_{cc_num}CC", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.EqCheckMRDefaultInverse()|config|{"eq_check_progress":False}))

        if not config.get("minimal", False):
            ModularMurphi(eq_rhs_clusters + eq_lhs_clusters, f"COMP_MR_EQP_L2sB_{cc_num}CC", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.EqCheckMRDefaultInverse()|config))


    return murphi_desc, def_path


def RunMurphiCheck(clusters: List[Cluster],
                   filename: str,
                   litmus_test: Union[LitmusTest, None] = None,
                   memory: int = 0,
                   custom_dir: str = '',
                   run_SSP: bool = False
                   ):
    murphi_desc, def_path = _run_murphi_modular_base(clusters, filename, litmus_test, run_SSP, custom_dir)

    if not memory:
        # Calculate the free memory in Megabyte
        memory = int(virtual_memory().free/2**20) - 8000      # Leave about 1GB of additional free memory

    sleep(0.10)
    murphi_desc.compile_and_run(memory)
    sleep(0.10)

    # Reset the path
    os.chdir(def_path)


def CompileMurphi(clusters: List[Cluster],
                  filename: str,
                  litmus_test: Union[LitmusTest, None] = None,
                  custom_dir: str = '',
                  run_SSP: bool = False
                  ):
    murphi_desc, def_path = _run_murphi_modular_base(clusters, filename, litmus_test, run_SSP, custom_dir)

    sleep(0.10)
    murphi_desc.compile()
    sleep(0.10)

    # Reset the path
    os.chdir(def_path)


def GenerateMurphi(clusters: List[Cluster],
                  filename: str,
                  litmus_test: Union[LitmusTest, None] = None,
                  custom_dir: str = '',
                  run_SSP: bool = False,
                  config: dict = {},
                #   eq_checks: bool = False,
                #   full_sys: bool = False,
                #   cc_num=2,
                #   minimal=False,
                #   prefetch_count=0,
                  ):

    murphi_desc, def_path = _run_murphi_modular_base(clusters, filename, litmus_test, run_SSP, custom_dir, config=config)
    sleep(0.10)

    murphi_desc.gen_make()

    # Reset the path
    os.chdir(def_path)
