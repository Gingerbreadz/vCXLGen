from Protocols.HieraHeteroGen.Ordered.RCCxCXLxRCC import RCCxCXLxRCC
from Protocols.HieraHeteroGen.Ordered.MESIxCXLxRCC import MESIxCXLxRCC
from Protocols.HieraHeteroGen.Ordered.MESIxCXLxMOESI import MESIxCXLxMOESI
from Protocols.HieraHeteroGen.Ordered.MESIxCXLxMESI import MESIxCXLxMESI
from Protocols.HieraHeteroGen.Ordered.MESIxCXL import MESIxCXL_HH
from Protocols.HieraHeteroGen.Ordered.MESIxMESIxMESI import MESIxMESIxMESI
from Protocols.HieraHeteroGen.Ordered.MESIxMOESIxMSI import MESIxMOESIxMSI
from Protocols.HieraHeteroGen.Ordered.MESIxMSI_HH import MESIxMSI_HH
from Protocols.HieraHeteroGen.Ordered.MESIxMESI_HH import MESIxMESI_HH
from Protocols.HieraHeteroGen.Ordered.MESIxMSIxMOESI import MESIxMSIxMOESI
from Protocols.HieraHeteroGen.Ordered.RCCOxMSI_HH import RCCOxMSI_HH

# TODO: REENABLE
# MESIxMESI_HH(eq_checks=True)
MESIxMESIxMESI()

# MESIxMESI_HH(cc_num=3, eq_checks=True)
# MESIxMESIxMESI(cc_num=3)

# MESIxCXL_HH(eq_checks=True)

MESIxCXLxMESI()
MESIxCXLxMOESI()
MESIxCXLxRCC()
RCCxCXLxRCC()
# MESIxCXLxRCC(cc_num=3)
# MESIxMSIxMOESI()
# MESIxMOESIxMSI()
