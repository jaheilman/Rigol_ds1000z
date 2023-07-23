import os
import numpy as _np
import tqdm as _tqdm
import pyvisa as _visa
from enum import Enum

# class Rigol_visa:
#     def __init__(self, visa_resource):
#         self.visa_resource = visa_resource
        
#     def visa_write(self, cmd):
#         self.visa_resource.write(cmd)

#     def visa_read(self):
#         return self.visa_resource.read().strip()

#     def visa_read_raw(self, num_bytes=-1):
#         return self.visa_resource.read_raw(num_bytes)

#     def visa_ask(self, cmd):
#         return self.visa_resource.query(cmd)

#     def visa_ask_raw(self, cmd, num_bytes=-1):
#         self.visa_write(cmd)
#         return self.visa_read_raw(num_bytes)

class Rigol_ds1000z():
    '''
    Rigol DS1000z series oscilloscope driver.

    Channels 1 through 4 (or 2 depending on the oscilloscope model) are accessed
    using `[channel_number]`.  e.g. osc[2] for channel 2.  Channel 1 corresponds
    to index 1 (not 0).

    Attributes:
        trigger (`_Rigol1000zTrigger`): Trigger object containing functions
            related to the oscilloscope trigger.
        timebase (`_Rigol1000zTimebase`): Timebase object containing functions
            related to the oscilloscope timebase.
    '''

    def __init__(self, visa_resource):
        self.visa_resource = visa_resource

        # self._channels = [_Rigol1000zChannel(c, self) for c in range(1,5)]
        # self.trigger = _Rigol1000zTrigger(self)
        # self.timebase = _Rigol1000zTimebase(self)
        self.acquire = _Rigol_ds1000z_Acquire(self)

    def __getitem__(self, i):
        assert 1 <= i <= 4, 'Not a valid channel.'
        return self._channels[i-1]

    def __len__(self):
        return len(self._channels)

    def visa_write(self, cmd):
        self.visa_resource.write(cmd)

    def visa_read(self):
        return self.visa_resource.read().strip()

    def visa_read_raw(self, num_bytes=-1):
        return self.visa_resource.read_raw(num_bytes)

    def visa_ask(self, cmd):
        return self.visa_resource.query(cmd)

    def visa_ask_raw(self, cmd, num_bytes=-1):
        self.visa_write(cmd)
        return self.visa_read_raw(num_bytes)

    def autoscale(self):
        self.visa_write(':autoscale') 

    def clear(self):
        self.visa_write(':clear')

    def run(self):
        self.visa_write(':run')

    def stop(self):
        self.visa_write(':stop')

    def single_shot(self):
        self.visa_write(':single')

    def force(self):
        self.visa_write(':tforce')


    # IEEE 488.2
    def cls(self):
        ''' 
        (IEEE 488.2)
        Clear all the event registers and clear the error queue.
        '''
        self.visa_write('*CLS')

    @property
    def ese(self) -> int:
        '''
        (IEEE 488.2)
        Set or query the enable register for the standard event status register set
        the range of <value> are the decimal numbers corresponding to 
        the binary numbers X0XXXX0X (X is 1 or 0).
        '''
        return self.visa_ask('*ESE?')
    @ese.setter
    def ese(self, val:int):
        self.visa_write(f'*ESE {val}')
    
    def esr(self) -> int:
        '''
        (IEEE 488.2)
        Query and clear the event register for the standard event status register.
        '''
        return self.visa_ask('*ESR?')

    def idn(self) -> str:
        '''
        (IEEE 488.2)
        Query the ID string of the instrument.
        '''
        return self.visa_ask('*IDN?')

    @property
    def opc(self) -> int:
        '''
        (IEEE 488.2)
        The *OPC command is used to set the Operation Complete bit (bit 0) in the standard
        event status register to 1 after the current operation is finished. The *OPC? command is
        used to query whether the current operation is finished.
        '''
        return self.visa_ask('*OPC?')
    @opc.setter
    def ese(self):
        self.visa_write('*OPC')

    def rst(self):
        '''
        (IEEE 488.2)
        Restore the instrument to the default state.
        '''
        self.visa_write('*RST')

    @property
    def sre(self) -> int:
        '''
        (IEEE 488.2)
        Set or query the enable register for the status byte register set.
        '''
        return self.visa_ask('*SRE?')
    @opc.setter
    def sre(self, val:int):
        self.visa_write(f'*SRE {val}')

    def stb(self) -> int:
        '''
        (IEEE 488.2)
        Query the event register for the status byte register. The value of the status byte register
        is set to 0 after this command is executed.
        
        The bit 0 and bit 1 of the status byte register are not used and are always treated as 0.
        The query returns the decimal numbers corresponding to the binary numbers X0XXXX0X
        (X is 1 or 0).
        '''
        return self.visa_ask('*STB?')
    
    def tst(self) -> int:
        '''
        (IEEE 488.2) 
        Perform a self-test and then return the seilf-test results.
        '''
        return self.visa_ask('*TST?')

    def wai(self):
        '''
        (IEEE 488.2)
        Wait for the operation to finish.
        '''
        self.visa_write('*WAI')
    

    
class _Rigol_ds1000z_Acquire:
    @property
    def averaging(self):
        '''
        Set or query the number of averages under the average acquisition mode

        count_n is an integer from 1 to 10
        '''
        return self.visa_ask(':acq:averages?')
    @averaging.setter
    def averaging(self, count_n:int):
        if count_n not in range(1, 11):
            return
        count = 2**count_n
        self.visa_write(f':acq:averages {count}')
        return

    @property
    def type(self):
        '''
        Set or query the acquisition mode of the oscilloscope.

        mode = {NORMal|AVERages|PEAK|HRESolution}
        '''
        return self.visa_ask(':acq:type?')
    @type.setter
    def type(self, mode:str):
        self.visa_write(f':acq:type {mode}')

    def mode_normal(self):
        self.type('NORM')

    def mode_averagesl(self):
        self.type('AVER')

    def mode_peak(self):
        self.type('PEAK')

    def mode_high_resolution(self):
        self.type('HRES')


    def sampling_rate(self):
        '''
        Query the current sample rate. The default unit is Sa/s.
        
        Sample rate is the sample frequency of the oscilloscope, namely the waveform points
        sampled per second.
        The following equation describes the relationship among memory depth, sample
        rate, and waveform length:
            Memory Depth = Sample Rate x Waveform Length
        Wherein, the Memory Depth can be set using the :ACQuire:MDEPth command, and
        the Waveform Length is the product of the horizontal timebase (set by
        the :TIMebase[:MAIN]:SCALe command) times the number of the horizontal scales
        (12 for DS1000Z).
        
        Return Format: The query returns the sample rate in float ~~scientific notation~~.
        '''
        return float(self.visa_ask(':acq:srat?'))

    @property
    def memory_depth(self):
        '''
        Set or query the memory depth of the oscilloscope (namely the number of waveform
        points that can be stored in a single trigger sample). The default unit is pts (points).

        For the analog channel:
        ― When a single channel is enabled, the range of <mdep> is 
        {AUTO|12000|120000|1200000|12000000|24000000}.
        ― When dual channels are enabled, the range of <mdep> is 
         {AUTO|6000|60000|600000|6000000|12000000}.
        ― When three/four channels are enabled, the range of <mdep> is 
          {AUTO|3000|30000|300000|3000000|6000000}.

        For the digital channel:
        ― When 8 channels are enabled, the range of <mdep> is 
          {AUTO|12000|120000|1200000|12000000|24000000}.
        ― When 16 channels are enabled, the range of <mdep> is
          {AUTO|6000|60000|600000|6000000|12000000}.
        
        The following equation describes the relationship among memory depth, sample
        rate, and waveform length:
           Memory Depth = Sample Rate x Waveform Length
        Wherein, the Waveform Length is the product of the horizontal timebase (set by
        the :TIMebase[:MAIN]:SCALe command) times the number of grids in the horizontal
        direction on the screen (12 for DS1000Z).
        When AUTO is selected, the oscilloscope will select the memory depth automatically
        according to the current sample rate.

        The query returns the actual number of points (integer) or AUTO.
        '''
        md = self.visa_ask(':acq:mdep?')
        return int(md) if md != 'AUTO' else md
    @memory_depth.setter
    def memory_depth(self, memory_depth):
        num_enabled_chans = sum(self.get_channels_enabled())
        # Restort to AUTO if improper number of pts specified
        if num_enabled_chans == 1:
            if pts not in ('AUTO', 12000, 120000, 1200000, 12000000, 24000000):
                pts = 'AUTO'
        elif num_enabled_chans == 2:
            if pts not in ('AUTO', 6000, 60000, 600000, 6000000, 12000000):
                pts = 'AUTO'
        elif num_enabled_chans in (3, 4):
            if pts not in ('AUTO', 3000, 30000, 300000, 3000000, 6000000):
                pts = 'AUTO'
        pts = int(pts) if pts != 'AUTO' else pts
        self.run()
        self.visa_write(f':acq:mdep {pts}')

class OneChannelMemoryOptions(Enum):
    AUTO          = 'AUTO',
    mdep_12000    = 12000,
    mdep_120000   = 120000,
    mdep_1200000  = 1200000,
    mdep_12000000 = 12000000,
    mdep_24000000 = 24000000

class TwoChannelMemoryOptions(Enum):
    AUTO          = 'AUTO',
    mdep_6000     = 6000,
    mdep_60000    = 60000,
    mdep_600000   = 600000,
    mdep_6000000  = 6000000,
    mdep_12000000 = 12000000

class FourChannelMemoryOptions(Enum):
    AUTO          = 'AUTO',
    mdep_3000     = 3000,
    mdep_30000    = 30000,
    mdep_300000   = 300000, 
    mdep_3000000  = 3000000, 
    mdep_6000000  = 6000000


class _Screenshot:
    def screenshot(self, filename = None, format='png'):
        '''
        Downloads a screenshot from the oscilloscope.

        Args:
            filename (str): The name of the image file.  The appropriate
                extension should be included (i.e. jpg, png, bmp or tif).
            type (str): The format image that should be downloaded.  Options
                are 'jpeg, 'png', 'bmp8', 'bmp24' and 'tiff'.  It appears that
                'jpeg' takes <3sec to download while all the other formats take
                <0.5sec.  Default is 'png'.
        '''

        assert format in ('jpeg', 'png', 'bmp8', 'bmp24', 'tiff')

        #Due to the up to 3s delay, we are setting timeout to None for this operation only
        oldTimeout = self.visa_resource.timeout
        self.visa_resource.timeout = None

        raw_img = self.visa_ask_raw(':disp:data? on,off,%s' % format, 3850780)[11:-4]

        self.visa_resource.timeout = oldTimeout

        if filename:
            try:
                os.remove(filename)
            except OSError:
                pass
            with open(filename, 'wb') as fs:
                fs.write(raw_img)

        return raw_img

class _Rigol_ds1000z_Channel(Rigol_ds1000z):
    @property
    def bandwidth_limit(self, chan):
        '''
        Set or query the number of averages under the average acquisition mode

        count_n is an integer from 1 to 10
        '''
        return self.visa_ask(f':CHAN{chan}:BWLimit?')
    @bandwidth_limit.setter
    def bandwidth_limit(self, chan:int, limit_on:bool=False):
        bw = '20M' if limit_on else 'OFF'
        self.visa_write(f':CHAN{chan}:BWLimit {bw}')
        return
    
    @property
    def coupling(self, chan):
        '''
        Set or query the coupling mode of the specified channel.

        chan {1|2|3|4}
        coupling  {AC|DC|GND} 
        '''
        return self.visa_ask(f':CHAN{chan}:COUPling?')
    @coupling.setter
    def coupling(self, chan:int, coupling:str):
        self.visa_write(f':CHAN{chan}:COUPling {coupling}')
        return
    
    @property
    def display(self, chan) -> str:
        '''
        Enable or disable the specified channel or query the status of the specified channel.

        chan {1|2|3|4}
        on {True|False} 

        Returns 1 (ON) or 0 (OFF) 
        '''
        return self.visa_ask(f':CHAN{chan}:DISPplay?')
    @display.setter
    def display(self, chan:int, channel_on:bool):
        chan_on = 1 if channel_on else 0
        self.visa_write(f':CHAN{chan}:DISPplay {chan_on}')
        return
    
    @property
    def invert(self, chan) -> int:
        '''
        Enable or disable the waveform invert of the specified channel or query the status of the
        waveform invert of the specified channel.

        chan {1|2|3|4}
        on {True|False} 

        Returns 0 (NORMAL) or 1 (INVERTED)  
        '''
        return self.visa_ask(f':CHAN{chan}:INVert?')
    @invert.setter
    def invert(self, chan:int, invert_on:bool):
        inv_chan = 1 if inv else 0
        self.visa_write(f':CHAN{chan}:INVert {inv_chan}')
        return
    
    @property
    def offset(self, chan) -> str:
        '''
        Set or query the vertical offset of the specified channel. The default unit is V.

        chan {1|2|3|4}
        <offset> 

        When the probe ratio is 1X,
            vertical scale≥500mV/div: -100V to +100V
            vertical scale<500mV/div: -2V to +2V
        When the probe ratio is 10X,
            vertical scale≥5V/div: -1000V to +1000V
            vertical scale<5V/div: -20V to +20V

        Returns offset in scientific notation [Volts] 
        '''
        return self.visa_ask(f':CHAN{chan}:OFFSet?')
    @offset.setter
    def offset(self, chan:int, offset_value:float):
        self.visa_write(f':CHAN{chan}:OFFSet {offset_value}')
        return

    @property
    def range(self, chan) -> str: 
        '''
        Set or query the vertical range of the specified channel. The default unit is V.

        This command indirectly modifies the vertical scale of the specified channel 
        (Vertical Scale = Vertical Range/8). 
        The vertical scale can be set by the :CHANnel<n>:SCALe command.

        <chan> {1|2|3|4}
        <scale> 

        When the probe ratio is 1X: 8mV to 80V
        When the probe ratio is 10X: 80mV to 800V

        Returns vertical scale in scientific notation [Volts] 
        '''
        return self.visa_ask(f':CHAN{chan}:RANGe?')
    @range.setter
    def range(self, chan:int, vertical_scale:float):
        self.visa_write(f':CHAN{chan}:RANGe {vertical_scale}')
        return
    
    @property
    def tcal(self, chan) -> str: # RANGE in SCPI, avoid conflict with python range()
        '''
        Set or query the delay calibration time of the specified channel to calibrate the zero offset
        of the corresponding channel. The default unit is s.

        <chan> {1|2|3|4}
        <val> can only be set to the specific values in the specified step. If the parameter you
        sent is not one of the specific values, the parameter will be set to the nearest specific
        values automatically. The step varies with the horizontal timebase (set by
        the :TIMebase[:MAIN]:SCALe command), as shown in the table below.
        Horizontal Timebase   | Step of the Delay Calibration Time
                        5ns   | 100ps
                        10ns  | 200ps
                        20ns  | 400ps
                        50ns  | 1ns
                        100ns | 2ns
                        200ns | 4ns
                        500ns | 10ns
                  1μs to 10μs | 20ns

        Returns delay in scientific notation [Volts] 

        Example:
        CHANnel1:TCAL 0.00000002 /*Set the delay calibration time to 20ns*/
        :CHANnel1:TCAL? /*The query returns 2.000000e-08*/
        '''
        return self.visa_ask(f':CHAN{chan}:TCAL?')
    @tcal.setter
    def tcal(self, chan:int, val:float):
        self.visa_write(f':CHAN{chan}:TCAL {val}')
        return
    
    @property
    def scale(self, chan) -> str:
        '''
        Set or query the vertical scale of the specified channel. The default unit is V.

        <chan> {1|2|3|4}
        <scale> 
        When the probe ratio is 1X: 1mV to 10V
        When the probe ratio is 10X (default): 10mV to 100V
        You can only set the vertical scale in 1-2-5 step, namely 10mV, 20mV, 50mV,
        100mV, …, 100V (the probe ratio is 10X). 

        You can use the :CHANnel<n>:VERNier command to enable or disable the fine
        adjustment of the vertical scale. By default, the fine adjustment is off. 
        When the fine adjustment is on, you can
        further adjust the vertical scale within a relatively smaller range to improve the
        vertical resolution. 

        Returns delay in scientific notation [Volts] 

        Example:
        CHANnel1:TCAL 0.00000002 /*Set the delay calibration time to 20ns*/
        :CHANnel1:TCAL? /*The query returns 2.000000e-08*/
        '''
        return self.visa_ask(f':CHAN{chan}:SCALe?')
    @scale.setter
    def scale(self, chan:int, scale_val:float):
        self.visa_write(f':CHAN{chan}:SCALe {scale_val}')
        return
    
    @property
    def probe(self, chan) -> int:
        '''
        Set or query the probe ratio of the specified channel.

        <chan> {1|2|3|4}
        <atten> {0.01|0.02|0.05|0.1|0.2|0.5|1|2|5|10|20|50|
                100|200|500|1000}  

        Returns the probe ratio in scientific notation.
        '''
        return self.visa_ask(f':CHAN{chan}:PROBe?')
    @probe.setter
    def probe(self, chan:int, atten:int):
        self.visa_write(f':CHAN{chan}:PROBe {atten}')
        return

    @property
    def units(self, chan) -> str:
        '''
        Set or query the amplitude display unit of the specified channel.

        <chan> {1|2|3|4}
        <units> {VOLTage|WATT|AMPere|UNKNown}   

        Returns VOLT, WATT, AMP, or UNKN
        '''
        return self.visa_ask(f':CHAN{chan}:UNITs?')
    @units.setter
    def units(self, chan:int, units:str):
        self.visa_write(f':CHAN{chan}:UNITs {units}')
        return
    
    @property
    def vernier(self, chan) -> str:
        '''
        Enable or disable the fine adjustment of the vertical scale of the specified channel,
        or query the fine adjustment status of the vertical scale of the specified channel.

        <chan> {1|2|3|4}
        <vernier_on> {True|False}
        When the fine adjustment is on, you can adjust the vertical scale within
        a relatively smaller range using CHAN:SCALE to improve the vertical resolution.  

        Returns 0 (OFF) or 1 (ON)
        '''
        return self.visa_ask(f':CHAN{chan}:VERNier?')
    @vernier.setter
    def vernier(self, chan:int, vernier_on:bool):
        vern_on = 1 if vernier_on else 0
        self.visa_write(f':CHAN{chan}:VERNier {vern_on}')
        return

# CURSor Commands
# The :CURSor commands are used to measure the X-axis value (such as time) and Y-axis value (such as
# voltage) of the waveform displayed on the screen.
# Command List:
#  :CURSor:MODE
#  :CURSor:MANual
#  :CURSor:TRACk
#  :CURSor:AUTO
#  :CURSor:XY

# CURSor:MANual
# Command List:
#  :CURSor:MANual:TYPE
#  :CURSor:MANual:SOURce
#  :CURSor:MANual:TUNit
#  :CURSor:MANual:VUNit
#  :CURSor:MANual:AX
#  :CURSor:MANual:BX
#  :CURSor:MANual:AY
#  :CURSor:MANual:BY
#  :CURSor:MANual:AXValue?
#  :CURSor:MANual:AYValue?
#  :CURSor:MANual:BXValue?
#  :CURSor:MANual:BYValue?
#  :CURSor:MANual:XDELta?
#  :CURSor:MANual:IXDELta?
#  :CURSor:MANual:YDELta?
# :CURSor:MANual:TYPE

# :CURSor:TRACk
# Command List:
#  :CURSor:TRACk:SOURce1
#  :CURSor:TRACk:SOURce2
#  :CURSor:TRACk:AX
#  :CURSor:TRACk:BX
#  :CURSor:TRACk:AY?
#  :CURSor:TRACk:BY?
#  :CURSor:TRACk:AXValue?
#  :CURSor:TRACk:AYValue?
#  :CURSor:TRACk:BXValue?
#  :CURSor:TRACk:BYValue?
#  :CURSor:TRACk:XDELta?
#  :CURSor:TRACk:YDELta?
#  :CURSor:TRACk:IXDELTA?

# :CURSor:AUTO
# Command List:
#  :CURSor:AUTO:ITEM
#  :CURSor:AUTO:AX?
#  :CURSor:AUTO:BX?
#  :CURSor:AUTO:AY?
#  :CURSor:AUTO:BY?
#  :CURSor:AUTO:AXValue?
#  :CURSor:AUTO:AYValue?
#  :CURSor:AUTO:BXValue?
#  :CURSor:AUTO:BYValue?

# DECoder Commands

# :MATH Commands

# MASK commands

class _Rigol_ds1000z_Measure(Rigol_ds1000z):

    @property
    def source(self) -> str:
        '''
        Set or query the source of the current measurement parameter.

        <source> {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                D9|D10|D11|D12|D13|D14|D15|
                CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH}
        '''
        return self.visa_ask(f':MEAS:SOURce?')
    @source.setter
    def source(self, source:str):
        self.visa_write(f':MEAS:SOURce {source}')
        return

    @property
    def counter_source(self) -> str:
        '''
        Set or query the source of the frequency counter, or disable the frequency counter. 

        <source> {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                D9|D10|D11|D12|D13|D14|D15|
                CHANnel1|CHANnel2|CHANnel3|CHANnel4|OFF}
        '''
        return self.visa_ask(f':MEAS:COUNter:SOURce?')
    @source.setter
    def source(self, source:str):
        self.visa_write(f'::MEAS:COUNter:SOURce {source}')
        return

    @property
    def counter_value(self, source) -> str:
        '''
        Query the measurement result of the frequency counter. The default unit is Hz

        The query returns the measurement result in scientific notation. 
        If the frequency counter is disabled, 0.0000000e+00 will be returned.
        Example -- :MEASure:COUNter:VALue? /*The query returns 1.000004e+03*/
        '''
        return self.visa_ask(f':MEAS:COUNter:VALue?')
    
    def clear(self, item:str):
        '''
        Clear one or all of the last five measurement items enabled
        <item> {ITEM1|ITEM2|ITEM3|ITEM4|ITEM5|ALL}
        '''
        self.visa_write(f':MEAS:CLEar {item}')
        return
    
    def clear(self, item:str):
        '''
        Recover the measurement item which has been cleared.
        <item> {ITEM1|ITEM2|ITEM3|ITEM4|ITEM5|ALL}
        '''
        self.visa_write(f':MEAS:RECover {item}')
        return

    @property
    def all_display(self) -> int:
        '''
        Enable or disable the all measurement function, 
        or query the status of the all measurement function. 

        <all_on> bool -> {{1|ON}|{0|OFF}}

        The all measurement function can measure the following 29 parameters of the
        source at the same time:
        Voltage Parameters: Vmax, Vmin, Vpp, Vtop, Vbase, Vamp, Vupper, Vmid, Vlower,
        Vavg, Vrms, Overshoot, Preshoot, Period Vrms, and Variance
        Time Parameters: Period, Frequency, Rise Time, Fall Time, +Width, -Width, +Duty,
        -Duty, tVmax, and tVmin
        Other Parameters: +Rate, -Rate, Area, and Period Area.
        The all measurement function can measure CH1, CH2, CH3, CH4, and the MATH
        channel at the same time. You can send the :MEASure:AMSource command to set
        the source of the all measurement function. 
        '''
        return self.visa_ask(f':MEAS:ADISplay?')
    @all_display.setter
    def all_display(self, all_on:bool):
        on = 1 if all_on else 0
        self.visa_write(f':MEAS:ADISplay {on}')
        return


    @property
    def amsource(self) -> int:
        '''
        Set or query the source(s) of the all measurement function

        <src> Discrete {CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH} 
        '''
        return self.visa_ask(f':MEAS:AMSource?')
    @amsource.setter
    def amsource(self, sources:list):
        src_list = ''
        for source in sources:
            src_list += source + ','
        src_list = src_list[0:-1] # drop trailing comma
        self.visa_write(f':MEAS:AMSource {src_list}')
        return

    @property
    def setup_max(self) -> int:
        '''
        Set or query the upper limit of the threshold
        (expressed in the percentage of amplitude) 
        in time, delay, and phase measurements.

        <value> Integer 7 to 95 (default 90)
        '''
        return self.visa_ask(f':MEAS:SETup:MAX?')
    @setup_max.setter
    def setup_max(self, upper_limit:int):
        if upper_limit < 7:
            upper_limit = 7 
        if upper_limit > 95:
            upper_limit = 95 
        self.visa_write(f':MEAS:SETup:MAX {upper_limit}')
        return

    @property
    def setup_mid(self) -> int:
        '''
        Set or query the middle point of the threshold
        (expressed in the percentage of amplitude)
        in time, delay, and phase measurements.
        
        The middle point must be lower than the upper limit and greater than the lower limit

        <value> Integer 6 to 94 (default 50)
        '''
        return self.visa_ask(f':MEAS:SETup:MID?')
    @setup_mid.setter
    def setup_mid(self, midpoint:int):
        if midpoint < 6:
            midpoint = 6 
        if midpoint > 94:
            midpoint = 94 
        self.visa_write(f':MEAS:SETup:MID {midpoint}')
        return

    @property
    def setup_min(self) -> int:
        '''
        Set or query the lower limit of the threshold
        (expressed in the percentage of amplitude)
        in time, delay, and phase measurements.
        
        The middle point must be lower than the upper limit and greater than the lower limit

        <value> Integer 6 to 94 (default 50)
        '''
        return self.visa_ask(f':MEAS:SETup:MIN?')
    @setup_min.setter
    def setup_min(self, lower_limit:int):
        if lower_limit < 5:
            lower_limit = 5 
        if lower_limit > 93:
            lower_limit = 93 
        self.visa_write(f':MEAS:SETup:MIN {lower_limit}')
        return

    @property
    def setup_psa(self) -> str:
        '''
        Set or query source A of Phase 1→2 and Phase 1→2 measurements.
        
        <source> Discrete
            {D0|D1|D2|D3|D4|D5|D6|D7|D8|
            D9|D10|D11|D12|D13|D14|D15|
            CHANnel1|CHANnel2|CHANnel3|CHANnel4}
        '''
        return self.visa_ask(f':MEAS:SETup:PSA?')
    @setup_psa.setter
    def setup_psa(self, source:str):
        self.visa_write(f':MEAS:SETup:PSA {source}')
        return

    @property
    def setup_psb(self) -> str:
        '''
        Set or query source B of Phase 1→2 and Phase 1→2 measurements.
        
        <source> Discrete
            {D0|D1|D2|D3|D4|D5|D6|D7|D8|
            D9|D10|D11|D12|D13|D14|D15|
            CHANnel1|CHANnel2|CHANnel3|CHANnel4}
        '''
        return self.visa_ask(f':MEAS:SETup:PSB?')
    @setup_psb.setter
    def setup_psb(self, source:str):
        self.visa_write(f':MEAS:SETup:PSB {source}')
        return

    @property
    def setup_dsa(self) -> str:
        '''
        Set or query source A of Delay 1→2 and Delay 1→2 measurements.
        
        <source> Discrete
            {D0|D1|D2|D3|D4|D5|D6|D7|D8|
            D9|D10|D11|D12|D13|D14|D15|
            CHANnel1|CHANnel2|CHANnel3|CHANnel4}
        '''
        return self.visa_ask(f':MEAS:SETup:DSA?')
    @setup_dsa.setter
    def setup_dsa(self, source:str):
        self.visa_write(f':MEAS:SETup:DSA {source}')
        return

    @property
    def setup_dsa(self) -> str:
        '''
        Set or query source B of Delay 1→2 and Delay 1→2 measurements.
        
        <source> Discrete
            {D0|D1|D2|D3|D4|D5|D6|D7|D8|
            D9|D10|D11|D12|D13|D14|D15|
            CHANnel1|CHANnel2|CHANnel3|CHANnel4}
        '''
        return self.visa_ask(f':MEAS:SETup:DSB?')
    @setup_dsa.setter
    def setup_dsa(self, source:str):
        self.visa_write(f':MEAS:SETup:DSB {source}')
        return
    

    @property
    def statistic_display(self) -> str:
        '''
        Enable or disable the statistic function, 
        or query the status of the statistic function. 
        
        <bool> Bool {{1|ON}|{0|OFF}} 0|OFF
        '''
        return self.visa_ask(f':MEAS:STATistic:DISPlay?')
    @statistic_display.setter
    def statistic_display(self, display_on:bool):
        disp_on = 1 if display_on else 0
        self.visa_write(f':MEAS:STATistic:DISPlay {disp_on}')
        return

    @property
    def statistic_display(self) -> str:
        '''
        Set or query the statistic mode. 
        
        <mode> Discrete {DIFFerence|EXTRemum} (Default EXTRem)
        '''
        return self.visa_ask(f':MEAS:STATistic:MODE?')
    @statistic_display.setter
    def statistic_display(self, mode:str):
        self.visa_write(f':MEAS:STATistic:MODE {mode}')
        return

    @property
    def statistic_reset(self) -> str:
        '''
        Clear the history data and make statistic again.
        
        <mode> Discrete {DIFFerence|EXTRemum} (Default EXTRem)
        '''
    def statistic_reset(self):
        self.visa_write(f':MEAS:STATistic:RESet')
        return

    @property
    def statistic_item(self) -> str:
        '''
        Enable the statistic function of any waveform parameter 
        of the specified source, or query the statistic result
        of any waveform parameter of the specified source.
        
        <item> Discrete
        {VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|
        VRMS|OVERshoot|PREShoot|MARea|MPARea|
        PERiod|FREQuency|RTIMe|FTIMe|PWIDth|
        NWIDth|PDUTy|NDUTy|RDELay|FDELay|
        RPHase|FPHase|TVMAX|TVMIN|PSLEWrate|
        NSLEWrate|VUPper|VMID|VLOWer|VARIance|
        PVRMS|PPULses|NPULses|PEDGes|NEDGes}
        --
        <src> Discrete Refer to Explanation
        <type> Discrete {MAXimum|MINimum|CURRent|AVERages|
        DEViation} --
        '''
        return self.visa_ask(f':MEAS:STATistic:MODE?')
    @statistic_item.setter
    def statistic_item(self, item:str):
        self.visa_write(f':MEAS:STATistic:MODE {item}')
        return

    @property
    def item(self) -> str:
        '''
        Measure any waveform parameter of the specified source, 
        or query the measurement result of any waveform 
        parameter of the specified source
        
        <item> Discrete
        {VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|
        VRMS|OVERshoot|PREShoot|MARea|MPARea|
        PERiod|FREQuency|RTIMe|FTIMe|PWIDth|
        NWIDth|PDUTy|NDUTy|RDELay|FDELay|
        RPHase|FPHase|TVMAX|TVMIN|PSLEWrate|
        NSLEWrate|VUPper|VMID|VLOWer|VARIance|
        '''
        return self.visa_ask(f':MEAS:STATistic:MODE?')
    @item.setter
    def item(self, item:str, sources=[]):
        if len(sources) > 1:
            for source in sources:
                item += "," + source
        self.visa_write(f':MEAS:ITEM {item}')
        return



















class noclassyet:
    def get_channels_enabled(self):
        return [c.enabled() for c in self._channels]

    




















class _Rigol1000zChannel:
    '''
    Handles the channels configuration (vertical axis).
    '''

    def __init__(self, channel, osc):
        self._channel = channel
        self._osc = osc

    def visa_write(self, cmd):
        return self._osc.visa_write(f':chan{self._channel}{cmd}')

    def visa_read(self):
        return self._osc.visa_read()

    def visa_ask(self, cmd):
        self.visa_write(cmd)
        r = self.visa_read()
        return r


    def enable(self):
        self.visa_write(':disp 1' % self._channel)
        return self.enabled()

    def disable(self):
        self.visa_write(':disp 0' % self._channel)
        return self.disabled()

    def enabled(self):
        return bool(int(self.visa_ask(':disp?')))

    def disabled(self):
        return bool(int(self.visa_ask(':disp?'))) ^ 1

    def get_offset_V(self):
        return float(self.visa_ask(':off?'))

    def set_offset_V(self, offset):
        assert -1000 <= offset <= 1000.
        self.visa_write(':off %.4e' % offset)
        return self.get_offset_V()

    def get_range_V(self):
        return self.visa_ask(':rang?')

    def set_range_V(self, range):
        assert 8e-3 <= range <= 800.
        self.visa_write(':rang %.4e' % range)
        return self.get_range_V()

    def set_vertical_scale_V(self, scale):
        assert 1e-3 <= scale <= 100
        self.visa_write(':scal %.4e' % scale)

    def get_probe_ratio(self):
        return float(self.visa_ask(':prob?'))

    def set_probe_ratio(self, ratio):
        assert ratio in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1,\
                         2, 5, 10, 20, 50, 100, 200, 500, 1000)
        self.visa_write(':prob %s' % ratio)
        return self.get_probe_ratio()

    def get_units(self):
        return self.visa_ask(':unit?')

    def set_units(self, unit):
        unit = unit.lower()
        assert unit in ('volt', 'watt', 'amp', 'unkn')
        self.visa_write(':unit %s' % unit)

    def get_data_premable(self):
        '''
        Get information about oscilloscope axes.

        Returns:
            dict: A dictionary containing general oscilloscope axes information.
        '''
        pre = self._osc.visa_ask(':wav:pre?').split(',')
        pre_dict = {
            'format': int(pre[0]),
            'type': int(pre[1]),
            'points': int(pre[2]),
            'count': int(pre[3]),
            'xincrement': float(pre[4]),
            'xorigin': float(pre[5]),
            'xreference': float(pre[6]),
            'yincrement': float(pre[7]),
            'yorigin': float(pre[8]),
            'yreference': float(pre[9]),
        }
        return pre_dict

    def get_data(self, mode='norm', filename=None):
        '''
        Download the captured voltage points from the oscilloscope.

        Args:
            mode (str): 'norm' if only the points on the screen should be
                downloaded, and 'raw' if all the points the ADC has captured
                should be downloaded.  Default is 'norm'.
            filename (None, str): Filename the data should be saved to.  Default
                is `None`; the data is not saved to a file.

        Returns:
            2-tuple: A tuple of two lists.  The first list is the time values
                and the second list is the voltage values.

        '''
        assert mode in ('norm', 'raw')

        # Setup scope
        self._osc.visa_write(f':stop')
        self._osc.visa_write(f':wav:sour chan{self._channel}')
        self._osc.visa_write(f':wav:mode {mode}')
        self._osc.visa_write(f':wav:form byte')

        info = self.get_data_premable()

        max_num_pts = 250000
        num_blocks = info['points'] // max_num_pts
        last_block_pts = info['points'] % max_num_pts

        datas = []
        for i in _tqdm.tqdm(range(num_blocks+1), ncols=60):
            if i < num_blocks:
                self._osc.visa_write(f':wav:star {(1+i*250000)}')
                self._osc.visa_write(f':wav:stop {(250000*(i+1))}')
            else:
                if last_block_pts:
                    self._osc.visa_write(f':wav:star {(1+num_blocks*250000)}')
                    self._osc.visa_write(f':wav:stop {(num_blocks*250000+last_block_pts)}')
                else:
                    break
            data = self._osc.visa_ask_raw(':wav:data?')[11:]
            data = _np.frombuffer(data, 'B')
            datas.append(data)

        datas = _np.concatenate(datas)
        v = (datas - info['yorigin'] - info['yreference']) * info['yincrement']

        t = _np.arange(0, info['points']*info['xincrement'], info['xincrement'])
        # info['xorigin'] + info['xreference']

        if filename:
            try:
                os.remove(filename)
            except OSError:
                pass
            _np.savetxt(filename, _np.c_[t, v], '%.12e', ',')

        return t, v

class _Rigol1000zTrigger:
    '''
    Handles the trigger configuration.
    '''

    def __init__(self, osc):
        self._osc = osc

    def get_trigger_level_V(self):
        return self._osc.visa_ask(':trig:edg:lev?')

    def set_trigger_level_V(self, level):
        self._osc.visa_write(':trig:edg:lev %.3e' % level)
        return self.get_trigger_level_V()

    def get_trigger_holdoff_s(self):
        return self._osc.visa_ask(':trig:hold?')

    def set_trigger_holdoff_s(self, holdoff):
        self._osc.visa_write(':trig:hold %.3e' % holdoff)
        return self.get_trigger_holdoff_s()

class _Rigol1000zTimebase:
    '''
    Handles the timebase configuration (horizontal axis).
    '''

    def __init__(self, osc):
        self._osc = osc

    def visa_write(self, cmd):
        return self._osc.visa_write(f':tim{cmd}')

    def visa_read(self):
        return self._osc.visa_read()

    def visa_ask(self, cmd):
        self.visa_write(cmd)
        r = self.visa_read()
        return r

    def get_timebase_scale_s_div(self):
        return float(self.visa_ask(':scal?'))

    def set_timebase_scale_s_div(self, timebase):
        assert 50e-9 <= timebase <= 50
        self.visa_write(':scal %.4e' % timebase)
        return self.get_timebase_scale_s_div()

    def get_timebase_mode(self):
        return self.visa_ask(':mode?')

    def set_timebase_mode(self, mode):
        mode = mode.lower()
        assert mode in ('main', 'xy', 'roll')
        self.visa_write(f':mode {mode}')
        return self.get_timebase_mode()

    def get_timebase_offset_s(self):
        return self.visa_ask(':offs?')

    def set_timebase_offset_s(self, offset):
        self.visa_write(':offs %.4e' % -offset)
        return self.get_timebase_offset_s()
