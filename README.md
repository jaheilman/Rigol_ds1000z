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

## Example
```python

from rigol_ds1000z import Rigol_ds1000z

# Autodetect Rigol ds1000z series
oscope = Rigol_ds1000z.rigol_ds1000z()
print(oscope.idn)

```

## Calling aditional commands
Most Rigol DS1000z SCPI commands are available in this library

Users can send SCPI commands and receive information directly from the oscilloscope through the following methods:

```python
todo

```

### Reading software measurements and statical data

```python
print(dso.measure.vmin(RigolTypes.MeasureSources.CHAN1))
print(dso.measure.vmax(RigolTypes.MeasureSources.CHAN1))
print(dso.measure.vpp(RigolTypes.MeasureSources.CHAN1))

```

An full implementation of a manual frequency sweep bode plot measurement is available in the _examples_ folder.


## Acknowledgements
Based on the original work by @jtambasco and @jeanyvesb9's change PyVISA dependency in order to make this library cross-platform.

I have added most of the SCPI commands, converted the interface into class property types.  
