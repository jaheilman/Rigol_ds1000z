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

# Autodetect the first 1000z series Rigol scopevisa finds
dso = rigol_ds1000z.Rigol_ds1000z()
print(dso.idn)

# Manually specify the scope: use if autodetect doesn't work
# or if you have more than one supported instrument attached
import pyvisa as visa

rm = visa.ResourceManager()
print(rm.list_resources())
visa_resource = rm.open_resource(rm.list_resources()[0])
dso_manual = Rigol_ds1000z(visa_resource=visa_resource)
print(dso_manual.idn)

# timebase
dso.timebase.scale = 5e-3 # set to 5ms

# Interact with your scope.
# Channels are accessed as an array indexed in range 1 - 4
dso.channel[1].display = RigolConst.OnOff.ON
dso.channel[1].probe = 1  # set probe to 1x
vertical_scale_1 = dso.channel[1].scale
print(f"Channel 1 vertical scale {vertical_scale_1}")
print(f"Channel 1 display state {dso.channel[1].display}") # will display "1" for ON

# Measurements are called by providing the channel as an argument to 
# the measurement helper function
chan1_vrms = dso.measure.vmin(RigolConst.MeasureSources.CHAN1)
chan1_vpeakpeak = dso.measure.vpp(RigolConst.MeasureSources.CHAN1)


```

## Calling library commands
Most Rigol DS1000z SCPI commands are available in this library.  The SCPI
functional groupings implmented are:
 - IEEE488
 - Acquire (ACQ)
 - Channel (CHAN)
 - Decoder (DEC)
 - Display (DISP)
 - Math (MATH)
 - Measure (MEAS)
 - Timebase (TIM)
 - Trigger (TRIG)
 - Wave (WAV)

These functions are all sub-classes of the Rigol_ds1000z class:
```python
dso = rigol_ds1000z.Rigol_ds1000z()
dso.acquire.<property>
dso.channel[n].<property>
dso.decoder[m].<property>
dso.display.<property>
```
and so on.

These are all implemented as sub-modules (e.g. rigol_ds1000z_measure.py) so you could 
instantiate and access them directly (albeit without auto-detect):

```python
from Rigol_ds1000z import rigol_ds1000z_measure
dso_measure = Rigol_ds1000z_Measure(visa_resource)
```

## About Constants
Many of the string literal arguments required for SCPI are stored in rigol_ds1000z_consants.

For example, a measurement requires the user specify which channel to measure, such as "CHAN1"
for the first analog channel, "D0" for the first digital channel (MSO scopes), or even "MATH"
for the math channel.  To assist with the syntax, the constants contain string-enum classes.

For example:

dso.measure.vmax(rigol_ds1000z_constants.MeasureSources.CHAN1) # = "CHAN1"

The type-hinting for the property will indicate the correct class to use.
These arguments can be supplied as strings that conform to the SCPI syntax.

The one exception to this is the OnOff enum, which is a traditional (integer) enum.  To the
DS1000z series, OFF = 0 and ON = 1, and while it accepts either in setting the value, a query
always returns the integer.

dso.channel[1].display = RigolConst.OnOff.ON
print(f"{dso.channel[1].display}") # prints "1"


## About Return values
While the Rigol SCPI commands and queries are always ASCII strings, sometimes the
responses are numerical: integers or floats, sometimes in scientific notation. 
This library will convert these to numbers.  Scientific notation will be converted to float.


## IEEE488
These commands are not nested in a sub-class

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
Measurements are the only commands that require two arguments: the measurement to make and the 
channel on which to make it. 

The library has helpers to reduce this to one argument - the channel.  
Here we use MeasureSources constants to access provide the correct channel syntax.

```python
ch1_min  = dso.measure.vmin(RigolConst.MeasureSources.CHAN1)
ch2_max  = dso.measure.vmax(RigolConst.MeasureSources.CHAN2)
ch3_pkpk = dso.measure.vpp(RigolConst.MeasureSources.CHAN3)
```

While the scope can only display five individual measurements, this can be ignored in remote control,
as the oldest measurement made will be replaced by the newest.

Not all measurements have helpers; in these cases call the base function
for measurements is measurement.item_get(MeasureType, MeasureSource)

```python
duty_cycle = dso.measure.item_get(RigolConst.Measurements.PDUTY, RigolConst.MeasureSources.CHAN4)
```

## Calling additional commands
Users can send SCPI commands and receive information directly from the oscilloscope through the rigol_visa module, and the following methods:

```python
my_idn = dso.visa.query("*IDN")

```


# Acknowledgements
Based on the original work by @jtambasco and @jeanyvesb9's change PyVISA dependency in order to make this library cross-platform.

I have added most of the SCPI commands, converted the interface into class property types.  
