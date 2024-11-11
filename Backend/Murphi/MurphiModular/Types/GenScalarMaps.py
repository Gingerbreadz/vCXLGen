from typing import List

from DataObjects.ClassCluster import Cluster

from Backend.Common.TemplateHandler.TemplateHandler import TemplateHandler
from Backend.Murphi.MurphiModular.MurphiTokens import MurphiTokens
from Backend.Murphi.BaseConfig import BaseConfig

from Debug.Monitor.ClassDebug import Debug
from Backend.Murphi.MurphiModular.Types.CheckTypes.GenPermType import GenPermType
from Backend.Murphi.MurphiModular.Types.CheckTypes.GenStoreMonitorType import GenStoreMonitorType


class GenScalarMaps(TemplateHandler, Debug):

    def __init__(self, murphi_str: List[str], clusters: List[Cluster], config: BaseConfig):
        TemplateHandler.__init__(self)
        Debug.__init__(self)

        scalar_maps = []

        if config.substitute_unions:
            for cluster in clusters:
                for arch in cluster.get_machine_architectures():
                    if cluster.get_machine_architecture_count(arch) > 1:
                        sm_str = MurphiTokens.k_sm + str(arch) + ": array[" + MurphiTokens.k_obj_set + str(arch) + "] of Machines" + self.end
                        scalar_maps.append(sm_str)

                


        murphi_str.append("----" + __name__.replace('.','/') + self.nl + self.add_tabs("".join(scalar_maps), 1) + self.nl)
