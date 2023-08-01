
from rigol_ds1000z import Rigol_ds1000z
import pyvisa as visa
import rigol_ds1000z_enums as ds_enum

rm = visa.ResourceManager()
print(rm.list_resources())
visa_resource = rm.open_resource(rm.list_resources()[0])

dso = Rigol_ds1000z(visa_resource)
print(dso.idn())

myval = dso.measure.vrms(ds_enum.MeasureSources.CHAN1)
print(myval)

myval = dso.measure.vmin(ds_enum.MeasureSources.CHAN1)
print(myval)

print(dso.measure.vmin(ds_enum.MeasureSources.CHAN2))
print(dso.measure.vmax(ds_enum.MeasureSources.CHAN2))
print(dso.measure.vpp(ds_enum.MeasureSources.CHAN2))

print(dso.measure.vmin(ds_enum.MeasureSources.CHAN1))
print(dso.measure.vmax(ds_enum.MeasureSources.CHAN1))
print(dso.measure.vpp(ds_enum.MeasureSources.CHAN1))

print('bye')