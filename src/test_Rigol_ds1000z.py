
from rigol_ds1000z import Rigol_ds1000z
import pyvisa as visa
import rigol_ds1000z_enums as ds_enum

rm = visa.ResourceManager()
print(rm.list_resources())
visa_resource = rm.open_resource(rm.list_resources()[0])

dso = Rigol_ds1000z(visa_resource)
print(dso.idn())

dso.measure.source = ds_enum.MeasureSource.CHAN1