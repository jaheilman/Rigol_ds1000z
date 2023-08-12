from .rigol_visa import Rigol_visa
import numpy as _np

class Rigol_ds1000z_Channel:
    '''
    Handles the channels configuration (vertical axis).
    One instance of this class should be instanciated for each channel
    '''

    def __init__(self, visa_resource, channel):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)
        self._chan = channel

    @property
    def bandwidth_limit(self) -> str:
        '''
        Set or query the bandwidth limit parameter of the specified channel.

        bw is {20M|OFF}
        '''
        return self.visa.query(f':CHAN{self._chan}:BWLimit?')
    @bandwidth_limit.setter
    def bandwidth_limit(self, limit_on:bool=False):
        bw = '20M' if limit_on else 'OFF'
        self.visa.write(f':CHAN{self._chan}:BWLimit {bw}')
        return
    
    @property
    def coupling(self):
        '''
        Set or query the coupling mode of the specified channel.

        chan {1|2|3|4}
        coupling  {AC|DC|GND} 
        '''
        return self.visa.query(f':CHAN{self._chan}:COUPling?')
    @coupling.setter
    def coupling(self, chan:int, coupling:str):
        self.visa.write(f':CHAN{self._chan}:COUPling {coupling}')
        return
    
    @property
    def display(self) -> str:
        '''
        Enable or disable the specified channel or query the status of the specified channel.

        chan {1|2|3|4}
        on {True|False} 

        Returns 1 (ON) or 0 (OFF) 
        '''
        return self.visa.query(f':CHAN{self._chan}:DISPplay?')
    @display.setter
    def display(self, channel_on:bool):
        chan_on = 1 if channel_on else 0
        self.visa.write(f':CHAN{self._chan}:DISPplay {chan_on}')
        return
    
    @property
    def invert(self) -> int:
        '''
        Enable or disable the waveform invert of the specified channel or query the status of the
        waveform invert of the specified channel.

        chan {1|2|3|4}
        on {True|False} 

        Returns 0 (NORMAL) or 1 (INVERTED)  
        '''
        return self.visa.query(f':CHAN{self._chan}:INVert?')
    @invert.setter
    def invert(self, invert_on:bool):
        inv_chan = 1 if invert_on else 0
        self.visa.write(f':CHAN{self._chan}:INVert {inv_chan}')
        return
    
    @property
    def offset(self) -> str:
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
        return self.visa.query(f':CHAN{self._chan}:OFFSet?')
    @offset.setter
    def offset(self, offset_value:float):
        self.visa.write(f':CHAN{self._chan}:OFFSet {offset_value}')
        return

    @property
    def range(self) -> str: 
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
        return float(self.visa.query(f':CHAN{self._chan}:RANGe?'))
    @range.setter
    def range(self, vertical_range:float):
        self.visa.write(f':CHAN{self._chan}:RANGe {vertical_range}')
        return
    
    @property
    def tcal(self) -> str: # RANGE in SCPI, avoid conflict with python range()
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
        return self.visa.query(f':CHAN{self._chan}:TCAL?')
    @tcal.setter
    def tcal(self, val:float):
        self.visa.write(f':CHAN{self._chan}:TCAL {val}')
        return
    
    @property
    def scale(self) -> str:
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
        return float(self.visa.query(f':CHAN{self._chan}:SCALe?'))
    @scale.setter
    def scale(self, vertical_scale:float):
        self.visa.write(f':CHAN{self._chan}:SCALe {vertical_scale}')
        return
    
    @property
    def probe(self) -> int:
        '''
        Set or query the probe ratio of the specified channel.

        <chan> {1|2|3|4}
        <atten> {0.01|0.02|0.05|0.1|0.2|0.5|1|2|5|10|20|50|
                100|200|500|1000}  

        Returns the probe ratio in scientific notation.
        '''
        return float(self.visa.query(f':CHAN{self._chan}:PROBe?'))
    @probe.setter
    def probe(self, atten:int):
        self.visa.write(f':CHAN{self._chan}:PROBe {atten}')
        return

    @property
    def units(self) -> str:
        '''
        Set or query the amplitude display unit of the specified channel.

        <chan> {1|2|3|4}
        <units> {VOLTage|WATT|AMPere|UNKNown}   

        Returns VOLT, WATT, AMP, or UNKN
        '''
        return self.visa.query(f':CHAN{self._chan}:UNITs?')
    @units.setter
    def units(self, units:str):
        self.visa.write(f':CHAN{self._chan}:UNITs {units}')
        return
    
    @property
    def vernier(self) -> str:
        '''
        Enable or disable the fine adjustment of the vertical scale of the specified channel,
        or query the fine adjustment status of the vertical scale of the specified channel.

        <chan> {1|2|3|4}
        <vernier_on> {True|False}
        When the fine adjustment is on, you can adjust the vertical scale within
        a relatively smaller range using CHAN:SCALE to improve the vertical resolution.  

        Returns 0 (OFF) or 1 (ON)
        '''
        return self.visa.query(f':CHAN{self._chan}:VERNier?')
    @vernier.setter
    def vernier(self, vernier_on:bool):
        vern_on = 1 if vernier_on else 0
        self.visa.write(f':CHAN{self._chan}:VERNier {vern_on}')
        return





