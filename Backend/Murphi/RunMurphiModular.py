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
                             eq_checks: bool = False
                             ) -> Tuple[ModularMurphi, str]:
    def_path = os.getcwd()

    path = "Murphi/"
    if custom_dir:
        path += custom_dir + '/'
    if litmus_test:
        path += litmus_test.test_name.split('.')[0]
    make_dir(path)

    # Generate Murphi file description
    murphi_desc = ModularMurphi(clusters, filename, False, litmus_test)

    # Rumur version that should be as similar to MURPHI as possible
    ModularMurphi(clusters, "RMR_" + filename, False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.RumurDefault()|{"remove_unused_channels":False}))

    if eq_checks:
        # Rumur version for the compositional verification, with abstractions on L2 & access based litmus tests for each L1
        ModularMurphi(clusters, "COMP_Model", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.RumurDefault()|{"eq_effective_mi_downgrade":True, "access_based_liveness":True}))

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
                            if "cacheL2" in system.arch.arch_name:
                                systems.append(rhs_system)
                            names.add(rhs_system.arch.arch_name)
                            
                eq_rhs_clusters.append(Cluster(tuple(systems), 'C2_RHS', False))

        ModularMurphi(eq_lhs_clusters + eq_rhs_clusters, "COMP_EQ_BsL2", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.EqCheckDefault()|{"eq_check_progress":False}))

        ModularMurphi(eq_lhs_clusters + eq_rhs_clusters, "COMP_EQP_BsL2", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.EqCheckDefault()))

        # Cache subset Directory

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
                            if "cacheL2" in system.arch.arch_name:
                                systems.append(lhs_system)
                            names.add(lhs_system.arch.arch_name)
                            
                eq_lhs_clusters.append(Cluster(tuple(systems), 'C2_LHS', False))

        ModularMurphi(eq_rhs_clusters + eq_lhs_clusters, "COMP_EQ_L2sB_", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.EqCheckDefaultInverse()|{"eq_check_progress":False}))

        ModularMurphi(eq_rhs_clusters + eq_lhs_clusters, "COMP_EQP_L2sB_", False, litmus_test, base_config=BaseConfig(clusters, litmus_test, config=BaseConfig.EqCheckDefaultInverse()))

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
                  eq_checks: bool = False
                  ):

    murphi_desc, def_path = _run_murphi_modular_base(clusters, filename, litmus_test, run_SSP, custom_dir, eq_checks=eq_checks)
    sleep(0.10)

    murphi_desc.gen_make()

    # Reset the path
    os.chdir(def_path)
