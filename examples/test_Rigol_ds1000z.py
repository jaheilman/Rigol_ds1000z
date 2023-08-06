
from rigol_ds1000z import Rigol_ds1000z
import pyvisa as visa
import rigol_ds1000z_enums as RigolTypes

# #manual set
rm = visa.ResourceManager()
print(rm.list_resources())
visa_resource = rm.open_resource(rm.list_resources()[0])
# dso = Rigol_ds1000z(visa_resource=visa_resource)


#autodetect
dso = Rigol_ds1000z()
print(dso.idn())
x=1

## Measurements
print(dso.measure.vmin(RigolTypes.MeasureSources.CHAN2))
print(dso.measure.vmax(RigolTypes.MeasureSources.CHAN2))
print(dso.measure.vpp(RigolTypes.MeasureSources.CHAN2))

print(dso.measure.vmin(RigolTypes.MeasureSources.CHAN1))
print(dso.measure.vmax(RigolTypes.MeasureSources.CHAN1))
print(dso.measure.vpp(RigolTypes.MeasureSources.CHAN1))

# Channels
print(dso.channel[1].range)
print(dso.channel[2].range)
print(dso.channel[1].scale)
print(dso.channel[2].scale)
print(dso.channel[1].probe)
print(dso.channel[2].probe)
dso.channel[1].probe = 1
dso.channel[2].probe = 10
print(dso.channel[1].probe)
print(dso.channel[2].probe)

# timebase
dso.timebase.scale = .005
print(dso.timebase.scale)
dso.timebase.scale = .003 # no effect b/c not 1-2-5
print(dso.timebase.scale)
dso.timebase.scale = .002
print(dso.timebase.scale)

# trigger
dso.trigger.mode = RigolTypes.TriggerMode.EDGE
dso.single
print(dso.acquire.memory_depth)
print(dso.acquire.sample_rate)
dso.run
print(dso.acquire.memory_depth)
print(dso.acquire.sample_rate)

data = dso.wave.get_wavedata(source=RigolTypes.WaveSource.CHAN2, mode=RigolTypes.WaveMode.NORMAL)
print(data)
print('bye')