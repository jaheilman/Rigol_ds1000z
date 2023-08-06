from Rigol_ds1000z import Rigol_ds1000z
import rigol_ds1000z_enums as RigolTypes

#autodetect
dso = Rigol_ds1000z()
print(dso.idn())

dso.trigger.mode = RigolTypes.TriggerMode.EDGE
dso.stop
print(dso.acquire.memory_depth)
print(dso.acquire.sample_rate)
dso.run

## Measurements
print(dso.measure.vmin(RigolTypes.MeasureSources.CHAN1))
print(dso.measure.vmax(RigolTypes.MeasureSources.CHAN1))
print(dso.measure.vpp(RigolTypes.MeasureSources.CHAN1))

# Channels
# channels 1-4 are accessed as an array
print(dso.channel[1].range)
print(dso.channel[1].scale)
dso.channel[1].probe = 1
print(dso.channel[1].probe)

print(dso.channel[2].range)
print(dso.channel[2].scale)
dso.channel[2].probe = 10
print(dso.channel[2].probe)

# timebase
dso.timebase.scale = 5e-3
print(dso.timebase.scale)

# wave
dso.single
data = dso.wave.get_wavedata(source=RigolTypes.WaveSource.CHAN2, mode=RigolTypes.WaveMode.NORMAL)
print(data)
