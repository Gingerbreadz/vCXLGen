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
import itertools
import multiprocessing
from typing import Union, Dict, List, Set, Tuple
from itertools import product
import os
import random
import time

from Parser.NetworkxParser.ClassProtoParser import ProtoParser

from DataObjects.ClassMachine import Machine
from DataObjects.ClassCluster import Cluster
from DataObjects.ClassLevel import Level

from Algorithms.ControllerGeneration.ProxyDirController.ClassProxyDirArchitecture import ProxyDirArchitecture
from Algorithms.ControllerGeneration.ProxyDirController.ClassHieraCacheArchitecture import HieraCacheArchitecture
from Algorithms.HeteroGen.ClassHHDirArchitecture import HHDirArchitecture
from Algorithms.ProtoAlgoNetworkx.ProtoNetworkxBase import ProtoNetworkxBase

from Algorithms.ControllerGeneration.CompoundBaseController.CompoundDirCacheArchitecture import CompoundDirCacheArchitecture

from MurphiLitmusTests.ClassLitmusTest import LitmusTest
from MurphiLitmusTests.ClassThreadMapLitmusTest import MachThreadMapLitmusTest
from MurphiLitmusTests.ClassLitmusInstruction import LoadInstruction
from Backend.Murphi.RunMurphiModular import RunMurphiCheck, GenerateMurphi, CompileMurphi

from Debug.Monitor.MakeDir import make_dir, dir_up
from Debug.Monitor.ClassDebug import Debug
from Debug.Monitor.ProtoCCTable import ProtoCCTablePrinter

class RunFullSystem(Debug):

    def __init__(self, default_system_model: bool = False):
        Debug.__init__(self, True)
        self.sys_name = ''
        self.default_system_model = default_system_model

    def run_test(self, filename_1: str, filename_2: str, filename_3: str, protocol_dir_path: str,
                 access_map_table1: List[Dict[str, List[str]]],
                 access_map_table2: List[Dict[str, List[str]]],
                 litmus_test_list_1: Union[LitmusTest, List[LitmusTest], None] = None,
                 litmus_test_list_2: Union[LitmusTest, List[LitmusTest], None] = None,
                 eq_checks = False,
                 cc_num = 2,
                 litmus = False
                 ):
        os.chdir(protocol_dir_path)
        protocol_1 = open(filename_1).read()
        protocol_2 = open(filename_2).read()
        protocol_3 = open(filename_3).read()
        self.sys_name = filename_1.split(".")[0] + "x" + filename_2.split(".")[0] + "x" + filename_3.split(".")[0]
        make_dir("FullSystem_NoCE")
        make_dir(self.sys_name)

        # Generate level based on given protocol and check input SSP
        level_1A = Level(ProtoParser(protocol_1, filename_1, False, True), "L1A")
        level_2A = Level(ProtoParser(protocol_2, filename_2, False, True), "L2")
        level_2B = Level(ProtoParser(protocol_2, filename_2, False, True), "L2")
        level_1B = Level(ProtoParser(protocol_3, filename_3, False, True), "L1B")

        # Generate higher level inter cluster protocol

        # For each cluster generate the connecting controllers

        # Generate the proxy caches, which are an input requirement to the HeteroGen controller
        # Proxy Cache interactions with the DIR are atomic, hence generate them before concurrency is generated
        # The new DirProxyCache replaces to original directory architecture in level_1

        # Generate HeteroGen
        hhgen_ctrl_a = HHDirArchitecture(level_1A, level_2A, access_map_table1, False)
        hhgen_ctrl_b = HHDirArchitecture(level_1B, level_2B, access_map_table2, False)

        # Run ProtoGen for each level
        #ProtoNetworkxBase(level_2)

        cache_machine_1A = Machine(level_1A.cache)
        directory_machine_2 = Machine(level_2A.directory) # Both 2A & 2B should work
        hhcache_machineA = Machine(level_1A.directory)
        cache_machine_1B = Machine(level_1B.cache)
        hhcache_machineB = Machine(level_1B.directory)
        cache_machine_2 = Machine(level_2A.cache)
        #cache_machine_2 = Machine(hhgen_ctrl_a.arch_tuple[1])

        cluster_1A = Cluster(
            tuple([cache_machine_1A] * cc_num) + tuple([hhcache_machineA]),
            'C1A', False)
        cluster_2 = Cluster(
            tuple([hhcache_machineA, hhcache_machineB, directory_machine_2]),
            'C2', False)
        cluster_1B = Cluster(
            tuple([cache_machine_1B] * cc_num) + tuple([hhcache_machineB]),
            'C1B', False)
        self.sys_list = {"C1A": filename_1.split(".")[0], "C2": filename_2.split(".")[0], "C1B": filename_3.split(".")[0]}

        #cluster_1.update_machine_archs(directory_machine_1.get_arch_list()[0], hhgen_ctrl_a)
        #cluster_2.update_machine_archs(hhcache_machine_2.get_arch_list()[0], hhgen_ctrl_a)

        if not litmus: # TODO: REENABLE, only disabled currently for quicker generation
            GenerateMurphi([cluster_1A, cluster_2, cluster_1B], f'FullSystem_{cc_num}CC', None, config={"eq_checks":eq_checks, "full_sys":True, "cc_num":cc_num, "sys_list": self.sys_list})

        #RunMurphiCheck([cluster_1], sys_name, None, 4000, 'DeadlockFreedom')
        #RunSLICCModular(cluster_1, sys_name)

        #self.verify_flat_protocols(cache_machine_1, cache_machine_2, directory_machine, self.sys_name, 4)

        cache_thread_dict: Dict[Machine, List[LitmusTest]] = {cache_machine_1A: litmus_test_list_1,
                                                             cache_machine_1B: litmus_test_list_2}

        if litmus_test_list_1 and litmus_test_list_2:
           self.run_full_litmus_test(self.sys_name, cache_thread_dict, directory_machine_2, hhcache_machineA, hhcache_machineB)
        #    self.run_comp_litmus_test(self.sys_name, cache_thread_dict, directory_machine_2, hhcache_machineA, hhcache_machineB)
        #    self.run_litmus_test(self.sys_name, cache_thread_dict, directory_machine_2, hhcache_machineA)

    def run_full_litmus_test(self, file_name: str, cache_thread_dict: Dict[Machine, List[LitmusTest]],
                        directory_machine: Machine, hhcache_machineA: Machine, hhcache_machineB: Machine):
        total_tests_generated = 0
        make_dir('Litmus_Tests')  # HACK VARIABLE
        
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:  # Use all available CPUs
            tasks = []

            # Get set of litmus test present in all architectures
            cache_thread_set = sorted(self.filter_common_litmus_tests(cache_thread_dict))
            for cache_thread in cache_thread_set:
                
                cache_mach_thread_dict = self.gen_cache_mach_thread_dict(cache_thread, cache_thread_dict)
                perm_list = self.gen_arch_perm_list(cache_mach_thread_dict)
                load_perm_list = self.gen_prefetch_load_permutations(cache_mach_thread_dict, 0)

                for load_perm in load_perm_list:
                    for ct_tuple_list in perm_list:
                        args = (cache_thread.split('.')[0], file_name, ct_tuple_list, load_perm, directory_machine, hhcache_machineA, hhcache_machineB)
                        # self.generate_full_litmus_test(file_name, ct_tuple_list, load_perm, directory_machine, hhcache_machineA, hhcache_machineB)
                        task = pool.apply_async(self.generate_full_litmus_test, args)
                        tasks.append(task)

                        total_tests_generated += 1
            
            for task in tasks:
                task.get()

        Debug.ptext(f'{total_tests_generated} Litmus tests were generated for {file_name} system')

    def generate_full_litmus_test(self, dir_name, file_name, ct_tuple_list, load_perm, directory_machine, hhcache_machineA, hhcache_machineB):
        result = '_'.join([str(node[0]).split('_')[-1] for node in ct_tuple_list])
        make_dir(dir_name)
        make_dir(result)
        # Generate the litmus test and the cluster from the permutation
        mach_litmus_test = MachThreadMapLitmusTest(ct_tuple_list[0][1].test_name, ct_tuple_list[0][1].exists)
        mach_list: List[Machine] = []
        for ct_tuple_ind in range(0, len(ct_tuple_list)):
            thread = ct_tuple_list[ct_tuple_ind][1].threads[ct_tuple_ind]. \
                new_prefetch_instructions_thread(load_perm[ct_tuple_ind])
            mach_litmus_test.add_cache_mach_thread_map(ct_tuple_list[ct_tuple_ind][0],
                                                       thread)
            mach_litmus_test.permutation_str_list.append(
                self.gen_thread_id_name(ct_tuple_list[ct_tuple_ind], ct_tuple_ind))
            mach_litmus_test.permutation_str_list.append(
                self.gen_thread_prefetch_name(load_perm[ct_tuple_ind]))
            mach_list.append(ct_tuple_list[ct_tuple_ind][0])

        cluster_1A = Cluster(
            tuple([mach for mach in mach_list if "1A" in str(mach)]) + tuple([hhcache_machineA]),
            'C1A', False)
        cluster_2 = Cluster(
            tuple([hhcache_machineA, hhcache_machineB, directory_machine]),
            'C2', False)
        cluster_1B = Cluster(
            tuple([mach for mach in mach_list if "1B" in str(mach)]) + tuple([hhcache_machineB]),
            'C1B', False)

        # Update the litmus test name
        litmus_test_thread_perm = '_'.join(mach_litmus_test.permutation_str_list)
        mach_litmus_test.test_name = mach_litmus_test.test_name.split('.')[0] + litmus_test_thread_perm

        # TODO double check if prefetch_count is determined corretly
        GenerateMurphi([cluster_1A, cluster_2, cluster_1B], file_name, mach_litmus_test, config={"minimal":True, "full_sys":True, "prefetch_count":len(load_perm[0]), "disable_eviction_for":"cache", "sys_list": self.sys_list})

        dir_up()
        dir_up()
    
    def run_comp_litmus_test(self, file_name: str, cache_thread_dict: Dict[Machine, List[LitmusTest]],
                        directory_machine: Machine, hhcache_machineA: Machine, hhcache_machineB: Machine):
        total_tests_generated = 0
        make_dir('Litmus_Tests')  # HACK VARIABLE
        
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:  # Use all available CPUs
            tasks = []

            # Get set of litmus test present in all architectures
            cache_thread_set = sorted(self.filter_common_litmus_tests(cache_thread_dict))
            for cache_thread in cache_thread_set:
                
                cache_mach_thread_dict = self.gen_cache_mach_thread_dict(cache_thread, cache_thread_dict)
                perm_list = self.gen_arch_perm_list(cache_mach_thread_dict)
                load_perm_list = self.gen_prefetch_load_permutations(cache_mach_thread_dict, 0)

                for load_perm in load_perm_list[:1]:
                    for ct_tuple_list in perm_list:
                        args = (cache_thread.split('.')[0], file_name, ct_tuple_list, load_perm, directory_machine, hhcache_machineA, hhcache_machineB)
                        # self.generate_full_litmus_test(file_name, ct_tuple_list, load_perm, directory_machine, hhcache_machineA, hhcache_machineB)
                        task = pool.apply_async(self.generate_full_litmus_test, args)
                        tasks.append(task)

                        total_tests_generated += 1
            
            for task in tasks:
                task.get()

        Debug.ptext(f'{total_tests_generated} Litmus tests were generated for {file_name} system')

    def generate_comp_litmus_test(self, dir_name, file_name, ct_tuple_list, load_perm, directory_machine, hhcache_machineA, hhcache_machineB):
        result = '_'.join([str(node[0]).split('_')[-1] for node in ct_tuple_list])
        make_dir(dir_name)
        make_dir(result)
        # Generate the litmus test and the cluster from the permutation
        mach_litmus_test = MachThreadMapLitmusTest(ct_tuple_list[0][1].test_name, ct_tuple_list[0][1].exists)
        mach_list: List[Machine] = []
        for ct_tuple_ind in range(0, len(ct_tuple_list)):
            thread = ct_tuple_list[ct_tuple_ind][1].threads[ct_tuple_ind]. \
                new_prefetch_instructions_thread(load_perm[ct_tuple_ind])
            mach_litmus_test.add_cache_mach_thread_map(ct_tuple_list[ct_tuple_ind][0],
                                                       thread)
            mach_litmus_test.permutation_str_list.append(
                self.gen_thread_id_name(ct_tuple_list[ct_tuple_ind], ct_tuple_ind))
            mach_litmus_test.permutation_str_list.append(
                self.gen_thread_prefetch_name(load_perm[ct_tuple_ind]))
            mach_list.append(ct_tuple_list[ct_tuple_ind][0])

        cluster_1A = Cluster(
            tuple([mach for mach in mach_list if "1A" in str(mach)]) + tuple([hhcache_machineA]),
            'C1A', False)
        cluster_2 = Cluster(
            tuple([mach for mach in mach_list if "1B" in str(mach)] + [hhcache_machineA, directory_machine]),
            'C2', False)

        # Update the litmus test name
        litmus_test_thread_perm = '_'.join(mach_litmus_test.permutation_str_list)
        mach_litmus_test.test_name = mach_litmus_test.test_name.split('.')[0] + litmus_test_thread_perm

        GenerateMurphi([cluster_1A, cluster_2], file_name, mach_litmus_test, minimal=True, full_sys=True)

        dir_up()
        dir_up()
    
    def run_litmus_test(self, file_name: str, cache_thread_dict: Dict[Machine, List[LitmusTest]],
                        directory_machine: Machine, hhcache_machineA: Machine):
        total_tests_generated = 0
        make_dir('Litmus_Tests')  # HACK VARIABLE
        # Get set of litmus test present in all architectures
        cache_thread_set = sorted(self.filter_common_litmus_tests(cache_thread_dict))
        for cache_thread in cache_thread_set:
            make_dir(cache_thread.split('.')[0])

            cache_mach_thread_dict = self.gen_cache_mach_thread_dict(cache_thread, cache_thread_dict)
            perm_list = self.gen_arch_perm_list(cache_mach_thread_dict)
            load_perm_list = self.gen_prefetch_load_permutations(cache_mach_thread_dict, 0)
            for load_perm in load_perm_list:
                for ct_tuple_list in perm_list:
                    self.generate_litmus_test(file_name, ct_tuple_list, load_perm, directory_machine, hhcache_machineA)
                    total_tests_generated += 1
            dir_up()

        Debug.ptext(f'{total_tests_generated} Litmus tests were generated for {file_name} system')

    def generate_litmus_test(self, file_name, ct_tuple_list, load_perm, directory_machine, hhcache_machineA):
        result = '_'.join([str(node[0]).split('_')[-1] for node in ct_tuple_list])
        make_dir(result)
        # Generate the litmus test and the cluster from the permutation
        mach_litmus_test = MachThreadMapLitmusTest(ct_tuple_list[0][1].test_name, ct_tuple_list[0][1].exists)
        mach_list: List[Machine] = []
        for ct_tuple_ind in range(0, len(ct_tuple_list)):
            thread = ct_tuple_list[ct_tuple_ind][1].threads[ct_tuple_ind]. \
                new_prefetch_instructions_thread(load_perm[ct_tuple_ind])
            mach_litmus_test.add_cache_mach_thread_map(ct_tuple_list[ct_tuple_ind][0],
                                                       thread)
            mach_litmus_test.permutation_str_list.append(
                self.gen_thread_id_name(ct_tuple_list[ct_tuple_ind], ct_tuple_ind))
            mach_litmus_test.permutation_str_list.append(
                self.gen_thread_prefetch_name(load_perm[ct_tuple_ind]))
            mach_list.append(ct_tuple_list[ct_tuple_ind][0])

        cluster_1A = Cluster(
            tuple([mach for mach in mach_list if "1A" in str(mach)]) + tuple([hhcache_machineA]),
            'C1A', False)
        cluster_2 = Cluster(
            tuple([mach for mach in mach_list if "2" in str(mach)]) + tuple([hhcache_machineA, directory_machine]),
            'C2', False)
        # cluster_1B = Cluster(
        #     tuple([mach for mach in mach_list if "1B" in str(mach)]) + tuple([hhcache_machineB]),
        #     'C1B', False)

        # Update the litmus test name
        litmus_test_thread_perm = '_'.join(mach_litmus_test.permutation_str_list)
        mach_litmus_test.test_name = mach_litmus_test.test_name.split('.')[0] + litmus_test_thread_perm

        GenerateMurphi([cluster_1A, cluster_2], file_name, mach_litmus_test, minimal=True, full_sys=True)

        dir_up()


    @staticmethod
    def gen_thread_id_name(ct_tuple: Tuple[Machine, LitmusTest], thread_id):
        return ct_tuple[1].memory_consistency_model + str(thread_id)

    @staticmethod
    def gen_thread_prefetch_name(load_perm: Tuple[LoadInstruction]):
        return '_p'+''.join(access.left_assign for access in load_perm)

    @staticmethod
    def filter_common_litmus_tests(cache_thread_dict: Dict[Machine, List[LitmusTest]]) -> Set[str]:
        cache_thread_set = set()
        for cache in cache_thread_dict:
            cache_thread_str_set = set(str(litmus_test) for litmus_test in cache_thread_dict[cache])
            if not cache_thread_set:
                cache_thread_set.update(cache_thread_str_set)
            else:
                cache_thread_set = cache_thread_set.intersection(cache_thread_str_set)
        return cache_thread_set

    @staticmethod
    def gen_cache_mach_thread_dict(cache_thread_type: str, cache_thread_dict: Dict[Machine, List[LitmusTest]]) -> \
            Dict[Machine, LitmusTest]:
        cache_mach_thread_dict: Dict[Machine, LitmusTest] = {}
        for cache in cache_thread_dict:
            for litmus_test in cache_thread_dict[cache]:
                if str(litmus_test) == cache_thread_type:
                    cache_mach_thread_dict[cache] = litmus_test
                    break
        return cache_mach_thread_dict

    @staticmethod
    def gen_arch_perm_list(cache_mach_thread_dict: Dict[Machine, LitmusTest]):
        thread_count = len(list(cache_mach_thread_dict.values())[0].threads)
        perm_elements = list(cache_mach_thread_dict.items())
        perm_list: List[Tuple[Tuple[Machine, LitmusTest], ...]] = \
            [prod for prod in product(perm_elements, repeat=thread_count)]
        return perm_list

    def gen_prefetch_load_permutations(self,
                                       cache_mach_thread_dict: Dict[Machine, LitmusTest], rand_sel_count: int = 0):
        litmus_test = list(cache_mach_thread_dict.values())[0]
        load_permutations = self.gen_simple_prefetch_loads(litmus_test)
        load_permutation_list = [prod for prod in product(load_permutations, repeat=len(litmus_test.threads))]

        if rand_sel_count == -1:
            return load_permutation_list

        sel_load_perm_list = [load_permutation_list[0], load_permutation_list[-1]]
        if rand_sel_count > 0:
            for ind in range(0, 2):
                sel_load_perm_list.append(load_permutation_list[random.randint(1, len(load_permutation_list)-2)])

        return sel_load_perm_list

    @staticmethod
    def gen_simple_prefetch_loads(litmus_test: LitmusTest):
        var_list = list(litmus_test.variable_adr_dict.keys())
        load_instr_list = [LoadInstruction(var, "") for var in var_list]
        load_combinations: List[List[LoadInstruction]] = []
        for ind in range(0, len(load_instr_list)+1):
            load_combinations += itertools.combinations(load_instr_list, ind)
        return load_combinations


