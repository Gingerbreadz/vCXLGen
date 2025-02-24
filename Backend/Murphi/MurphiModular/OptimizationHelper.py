
from Backend.Murphi.BaseConfig import BaseConfig


class OptimizationHelper:

    supported_nets = ["req", "req2", "resp", "fwd", "rwd", "birsp", "bisnp", "drs", "ndr"]

    def has_arch_net(arch: str, net: str, config: BaseConfig):
        if not config.remove_unused_channels:
            return True

        if net not in OptimizationHelper.supported_nets:
            breakpoint() 
            assert False # unknown net

        if "cache" in arch and net == "req":
            return False
        if "dir" in arch and "L2" in arch and net == "fwd":
            return False
        
        for cl in config.sys_list:
            if cl in arch or cl.replace("C", "L") in arch:
                if config.sys_list[cl] in ["MSI", "MESI", "MOESI", "RCCHetero"]:
                    if "cache" in arch or "L2" in arch:
                        if net in ["req2", "rwd", "birsp", "bisnp", "drs", "ndr"]:
                            return False

        return True
    
    def can_arch_recieve(arch: str, net: str, cluster: str, config: BaseConfig):

        if net not in OptimizationHelper.supported_nets:
            breakpoint() 
            assert False # unknown net

        if "cache" in arch and net == "req":
            return False
        if "dir" in arch and "L2" in arch and net == "fwd":
            return False
        if "dir" in arch and "L1" in arch and net == "fwd" and "1" in cluster:
            return False
        if "dir" in arch and "L1" in arch and net == "req" and "2" in cluster:
            return False
        
        if cluster in config.sys_list:
            if config.sys_list[cluster] in ["MSI", "MESI", "MOESI", "RCCHetero"]:
                if net in ["req2", "rwd", "birsp", "bisnp", "drs", "ndr"]:
                    return False
        
        return True