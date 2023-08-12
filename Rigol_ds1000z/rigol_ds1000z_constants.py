from enum import auto
from strenum import StrEnum

'''
A Class declared with (StrEnum) allows use of auto()
CHAN1 = auto()
which sets the string equal to the property name, equivalent to
CHAN1 = "CHAN1"
'''

class MeasureSources(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
    OFF = auto()
    D0 = auto()
    D1 = auto()
    D2 = auto()
    D3 = auto()
    D4 = auto()
    D5 = auto()
    D6 = auto()
    D7 = auto()
    D8 = auto()
    D9 = auto()
    D10 = auto()
    D11 = auto()
    D12 = auto()
    D13 = auto()
    D14 = auto()
    D15 = auto()

class AnalogChannels(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
    MATH = auto()


class MeasureStatisticsDisplay(StrEnum):
    difference = "DIFF"
    extremum = "EXTR"
    DIFF = auto()
    EXTR = auto()

## These from :MEAS:ADIS
class MeasureItems(StrEnum):
    ITEM1 = auto()
    ITEM2 = auto()
    ITEM3 = auto()
    ITEM4 = auto()
    ITEM5 = auto()
    ALL = auto()

class Measurements(StrEnum):
    VMAX = auto()
    VMIN = auto()
    VPP = auto()
    v_peak_to_peak = "VPP"
    VTOP = auto()
    VBASE = auto()
    VAMP = auto()
    VAVG = auto()
    VRMS = auto()
    OVERSHOOT = auto()
    PRESHOOT = auto()
    MAREA = auto()
    MPAREA = auto()
    PERIOD = auto()
    FREQUENCY = auto()
    RTIME = auto()
    FTIME = auto()
    PWIDTH = auto()
    NWIDTH = auto()
    PDUTY = auto()
    NDUTY = auto()
    RDELAY = auto()
    FDELAY = auto()
    RPHASE = auto()
    FPHASE = auto()
    TVMAX = auto()
    TVMIN = auto()
    PSLEWRATE = auto()
    NSLEWRATE = auto()
    VUPPER = auto()
    VMID = auto()
    VLOWER = auto()
    VARIANCE = auto()
    PVRMS = auto()
    PPULSES = auto()
    NPULSES = auto()
    PEDGES = auto()
    NEDGES = auto()

class TriggerMode(StrEnum):
    EDGE = auto()
    PULSE = auto()
    RUNT = auto()
    WIND = auto()
    NEDG = auto()
    SLOPE = auto()
    VIDEO = auto()
    PATTERN = auto()
    DELAY = auto()
    TIMEOUT = auto()
    DURATION = auto()
    SHOLD = auto()
    RS232 = auto()
    IIC = auto()
    SPI = auto()

class WaveSource(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
    OFF = auto()
    D0 = auto()
    D1 = auto()
    D2 = auto()
    D3 = auto()
    D4 = auto()
    D5 = auto()
    D6 = auto()
    D7 = auto()
    D8 = auto()
    D9 = auto()
    D10 = auto()
    D11 = auto()
    D12 = auto()
    D13 = auto()
    D14 = auto()
    D15 = auto()
    MATH = auto()

class WaveMode(StrEnum):
    NORMAL = auto()
    MAXIMUM = auto()
    RAW = auto()

class MemoryDepth(StrEnum):
    AUTO           = 'AUTO'
    Analog_1Chan_12k    = '12000'
    Analog_1Chan_120k   = '120000'
    Analog_1Chan_1M2    = '1200000'
    Analog_1Chan_12M    = '12000000'
    Analog_1Chan_24M    = '24000000'
    Analog_2Chan_6k     = '6000'
    Analog_2Chan_60k    = '60000'
    Analog_2Chan_600k   = '600000'
    Analog_2Chan_6M     = '6000000'
    Analog_2Chan_12M    = '12000000'
    Analog_4Chan_3k     = '3000'
    Analog_4Chan_30k    = '30000'
    Analog_4Chan_300k   = '300000'
    Analog_4Chan_3M     = '3000000' 
    Analog_4Chan_6M     = '6000000'
    Digital_8Chan_12k   = '12000' 
    Digital_8Chan_120k  = '120000'
    Digital_8Chan_1M2   = '1200000'
    Digital_8Chan_12M   = '12000000'
    Digital_8Chan_24M   = '24000000'
    Digital_16Chan_6k   = '6000'
    Digital_16Chan_60k  = '60000'
    Digital_16Chan_600k = '600000'
    Digital_16Chan_6M   = '6000000'
    Digital_16Chan_12M  = '12000000'


class AcquisitionMode(StrEnum):
    NORMAL = auto()
    AVERAGES = auto()
    PEAK = auto()
    HIGH_RESOLUTION = "HResolution"

class DecoderMode(StrEnum):
    PARALLEL = auto()
    UART = auto()
    SPI = auto()
    IIC = auto()

class DecoderFormat(StrEnum):
    HEX = auto()
    ASCII = auto()
    DEC = auto()
    BIN = auto()
    LINE = auto()

class DecoderUart(StrEnum):
    D0 = auto()
    D1 = auto()
    D2 = auto()
    D3 = auto()
    D4 = auto()
    D5 = auto()
    D6 = auto()
    D7 = auto()
    D8 = auto()
    D9 = auto()
    D10 = auto()
    D11 = auto()
    D12 = auto()
    D13 = auto()
    D14 = auto()
    D15 = auto()
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
    OFF = auto()

class UartParity(StrEnum):
    NONE = auto()
    EVEN = auto()
    ODD = auto()