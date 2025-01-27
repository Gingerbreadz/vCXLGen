
from Backend.Murphi.BaseConfig import BaseConfig


class OptimizationHelper:

    def has_arch_net(arch: str, net: str, config: BaseConfig):
        if not config.remove_unused_channels:
            return True

        if net not in ["req", "resp", "fwd"]:
            breakpoint() 
            assert False # unknown net

        if "cache" in arch and net == "req":
            return False
        if "dir" in arch and "L2" in arch and net == "fwd":
            return False
        
        return True