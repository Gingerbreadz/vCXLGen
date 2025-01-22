from Protocols.HieraHeteroGen.Ordered.MESIxMESIxMESI import MESIxMESIxMESI
from Protocols.HieraHeteroGen.Ordered.MESIxMSI_HH import MESIxMSI_HH
from Protocols.HieraHeteroGen.Ordered.MESIxMESI_HH import MESIxMESI_HH
from Protocols.HieraHeteroGen.Ordered.RCCOxMSI_HH import RCCOxMSI_HH

MESIxMESI_HH(eq_checks=True)
MESIxMESIxMESI()

MESIxMESI_HH(cc_num=3, eq_checks=True)
MESIxMESIxMESI(cc_num=3)

