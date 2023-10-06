from enum import Enum, auto
from strenum import StrEnum

'''
A Class declared with (StrEnum) allows use of auto()
CHAN1 = auto()
which sets the string equal to the property name, equivalent to
CHAN1 = "CHAN1"
'''

def class_has_value(test_value, in_class) -> bool:
    values = set(item.value for item in in_class)
    return test_value in values

class AcquisitionMode(StrEnum):
    NORMAL = auto()
    AVERAGES = auto()
    PEAK = auto()
    HIGH_RESOLUTION = "HResolution"


class AnalogChannels(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
    MATH = auto()

class AnalogSources(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()

class ChannelCoupling(StrEnum):
    AC = auto()
    DC = auto()
    GND = auto()

class ChannelUnits(StrEnum):
    VOLT = auto()
    WATT = auto()
    AMP  = auto()
    UNKN = auto()

class DecoderChannel(StrEnum):
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

class DecoderFormat(StrEnum):
    HEX = auto()
    ASCII = auto()
    DEC = auto()
    BIN = auto()
    LINE = auto()

class DecoderMode(StrEnum):
    PARALLEL = auto()
    UART = auto()
    SPI = auto()
    IIC = auto()

class DisplayGradingTime(StrEnum):
    MIN = "MIN"
    T100ms = "0.1"
    T200ms = "0.2"
    T500ms = "0.5"
    T1s    = "1"
    T5s    = "2"
    T10s   = "10"
    INFINITE = "INF"

class DisplayGridTypes(StrEnum):
    FULL = auto()
    HALF = auto()
    NONE = auto()

class DisplayTypes(StrEnum):
    VECTORS = "VECT"
    DOTS = "DOT"

class Edge(StrEnum):
    RISE = auto()
    FALL = auto()
    BOTH = auto()

class Endianess(StrEnum):
    LSB = auto()
    MSB = auto()

class FFTMode(StrEnum):
    TRACE = "TRAC"
    MEMORY = "MEM"

class FFTSources(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()

class FFTUnits(StrEnum):
    VRMS = auto()
    DB = auto()

class FFTWindows(StrEnum):
    RECTANGLE = "RECT"
    BLACKMAN = "BLAC"
    HANNING = "HANN"
    HAMMING = "HAMM"
    FLATTOP = "FLAT"
    TRIANGLE = "TRI"

class FxOperations(StrEnum):
    ADD = "ADD"
    SUBTRACT = "SUBT"
    MULTPLY = "MULT"
    DIVIDE = "DIV"

class I2CAddressMode(StrEnum):
    NORMAL = auto()
    RW = auto()

class MathOperations(StrEnum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVISION = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    NOT = auto()
    FFT = auto()
    INTG = auto()
    DIFF = auto()
    SQRT = auto()
    LOG = auto()
    LN = auto()
    EXP = auto()
    ABS = auto()
    FILTER  = auto()

class LogicSources(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
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

class MathSources(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
    FX = auto()

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

class MeasureStatisticsDisplay(StrEnum):
    difference = "DIFF"
    extremum = "EXTR"
    DIFF = auto()
    EXTR = auto()

class MeasureStatisticsType(StrEnum):
    MAXIMUM   = auto()
    MINIMUM   = auto()
    CURRENT   = auto()
    AVERAGES  = auto()
    DEVIATION = auto()


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



class OnOff(Enum):
    ON = 1
    OFF = 0

class Polarity(StrEnum):
    POSITIVE = "POS"
    NEGATIVE = "NEG"

class SpiEdge(StrEnum):
    RISE = auto()
    FALL = auto()

class SpiTimeout(StrEnum):
    TIM = auto()
    CS  = auto()

class StatisticsMode(StrEnum):
    DIFFERENCE = "DIFF" 
    EXTREMUM = "EXTR"

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

class UartStopBits(StrEnum):
    Bits_1   = "1"
    Bits_1_5 = "1.5"
    Bits_2   = "2"
    
class UartParity(StrEnum):
    NONE = auto()
    EVEN = auto()
    ODD = auto()

class WaveFormat(StrEnum):
    WORD = auto()
    BYTE = auto()
    ASCII = auto()


class WaveMode(StrEnum):
    NORMAL = auto()
    MAXIMUM = auto()
    RAW = auto()

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

