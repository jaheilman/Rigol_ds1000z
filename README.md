# Rigol_ds1000z
Python library to control Rigol DS1000z series oscilloscopes based on the VISA protocol (PyVISA). The oscilloscope can be connected either by USB or by Ethernet to the local network (See PyVISA docs for more information).

Syntax follows the Rigol DS1000Z programming reference, where SCPI commands are made pythonic. 

Currently supports the following:
  Acquire
  Channel
  Cursor
  Measure
  Screenshot
  Timebase
  Trigger (partial)
  Wave

There are also enums present to assist string settings:
  Measurements 

Tested on Linux Mint and MX Linux using a Rigol DS1154Z.

## Dependencies
* [numpy](https://github.com/numpy/numpy)
* [pyvisa](https://github.com/pyvisa/pyvisa)
* [strenum](https://github.com/irgeek/StrEnum)

# Example
```python

from Rigol_ds1000z import rigol_ds1000z
import Rigol_ds1000z.rigol_ds1000z_constants as RigolConst

# Autodetect a Rigol scope of 1000z series model
dso = rigol_ds1000z.Rigol_ds1000z()
print(dso.idn)

# Manually select a scope
import pyvisa as visa

rm = visa.ResourceManager()
print(rm.list_resources())
visa_resource = rm.open_resource(rm.list_resources()[0])
dso_manual = Rigol_ds1000z(visa_resource=visa_resource)
print(dso_manual.idn)
```

## Calling library commands
Most Rigol DS1000z SCPI commands are available in this library.  The SCPI
functional groupings implmented are:
 - IEEE488
 - Acquire (ACQ)
 - Channel (CHAN)
 - Measure (MEAS)
 - Timebase (TIM)
 - Trigger (TRIG)
 - Wave (WAV)

These are all implemented as sub-modules (e.g. rigol_ds1000z_measure.py), but
are all included in the main class, Rigol_ds1000z, and nest nicely.

Also, many of the string types required for commands are stored in rigol_ds1000z_consants.

## IEEE488 
```python
dso.idn
dso.run
```

## Example Acquire
```python
sample_rate = dso.acquire.sample_rate
print(sample_rate)
dso.acquire.averages = 2
```

## Measurements
Here we use MeasureSources constants to access provide the correct channel syntax.
```python
voltage_min  = dso.measure.vmin(RigolConst.MeasureSources.CHAN1)
voltage_max  = dso.measure.vmax(RigolConst.MeasureSources.CHAN2)
voltage_pkpk = dso.measure.vpp(RigolConst.MeasureSources.CHAN3)
```
## Calling additional commands
Users can send SCPI commands and receive information directly from the oscilloscope through the rigol_visa module, and the following methods:

```python
my_idn = dso.visa.query("*IDN")

```


# Acknowledgements
Based on the original work by @jtambasco and @jeanyvesb9's change PyVISA dependency in order to make this library cross-platform.

I have added most of the SCPI commands, converted the interface into class property types.  
