
from typing import Dict, List, Set
from Backend.Murphi.BaseConfig import BaseConfig
from DataObjects.ClassCluster import Cluster


class EqCheckHelper:

    systemStates = ["systemLHS", "systemRHS", "systemLHSExt", "systemRHSExt" ]

    def get_type(elem: str) -> str:
        return elem.split("_")[0]

    def get_machine_types(clusters: List[Cluster]) -> List[str]:
        archs = set()
        for cluster in clusters:
            archs.update(set(machine.arch for machine in cluster.system_tuple))

        return list(set([ str(x) for x in list(archs)]))
    
    def get_machines(clusters: List[Cluster]) -> List[str]:
        archs = set()
        for cluster in clusters:
            for arch in cluster.get_machine_architectures():
                mach_count = cluster.get_machine_architecture_count(arch)
                for i in range(mach_count):
                    archs.add(str(arch) + "_" + str(i))

        return list(archs)

    def get_state_assoc(systemStates: List[str], machines: List[str], config: BaseConfig) -> Dict[str, Set[str]]:
        assoc = {}
        for state in systemStates:
            assoc[state] = set()

        for machine in machines:
            if config.use_mrecords:
                machine = EqCheckHelper.get_type(machine)

            assoc[EqCheckHelper.get_machine_state(machine, config)].add(machine)
            
        return assoc

    def get_machine_state(machine: str, config: BaseConfig) -> bool:
        if config.use_mrecords:
            machine = EqCheckHelper.get_type(machine)

        if machine == config.eq_lhs:
            return "systemLHS"
        elif machine == config.eq_rhs: 
            return "systemRHS"
        elif "L1" in machine:
            if "LHS" in machine:
                return "systemLHS"
            elif "RHS" in machine:
                return "systemRHS"
        elif "L2" in machine:
            if "LHS" in machine:
                return "systemLHSExt"
            elif "RHS" in machine:
                return "systemRHSExt"

        assert False, "can not associate machine with any system state"