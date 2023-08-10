from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import MeasureItems, MeasureSources, Measurements, AnalogChannels
from typing import List

class Rigol_ds1000z_Measure():
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)
    
    @property
    def source(self) -> str:
        '''
        Set or query the source of the current measurement parameter.

        <source> {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                D9|D10|D11|D12|D13|D14|D15|
                CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH}
        '''
        return self.visa.query(f':MEAS:SOURce?')
    @source.setter
    def source(self, source:MeasureSources):
        s = source.value
        self.visa.write(f':MEAS:SOURce {s}')
        return

    @property
    def counter_source(self) -> str:
        '''
        Set or query the source of the frequency counter, or disable the frequency counter. 

        <source> {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                  D9|D10|D11|D12|D13|D14|D15|
                  CHANnel1|CHANnel2|CHANnel3|CHANnel4|OFF}
        '''
        return self.visa.query(f':MEAS:COUNter:SOURce?')
    @source.setter
    def source(self, source:MeasureSources):
        s = source.value
        self.visa.write(f':MEAS:COUNter:SOURce {s}')
        return

    @property
    def counter_value(self) -> str:
        '''
        Query the measurement result of the frequency counter. The default unit is Hz

        The query returns the measurement result in scientific notation. 
        If the frequency counter is disabled, 0.0000000e+00 will be returned.
        Example -- :MEASure:COUNter:VALue? /*The query returns 1.000004e+03*/
        '''
        return self.visa.query(f':MEAS:COUNter:VALue?')
    
    def clear(self, item:MeasureItems):
        '''
        Clear one or all of the last five measurement items enabled
        <item> {ITEM1|ITEM2|ITEM3|ITEM4|ITEM5|ALL}
        '''
        self.visa.write(f':MEAS:CLEar {item}')
        return
    
    def clear(self, item:MeasureItems):
        '''
        Recover the measurement item which has been cleared.
        <item> {ITEM1|ITEM2|ITEM3|ITEM4|ITEM5|ALL}
        '''
        self.visa.write(f':MEAS:RECover {item}')
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
        return self.visa.query(f':MEAS:ADISplay?')
    @all_display.setter
    def all_display(self, all_on:bool):
        on = 1 if all_on else 0
        self.visa.write(f':MEAS:ADISplay {on}')
        return


    @property
    def amsource(self) -> int:
        '''
        Set or query the source(s) of the all measurement function

        <src> Discrete {CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH} 
        '''
        return self.visa.query(f':MEAS:AMSource?')
    @amsource.setter
    def amsource(self, sources:List[AnalogChannels]):
        src_list = ''
        for source in sources:
            src_list += source + ','
        src_list = src_list[0:-1] # drop trailing comma
        self.visa.write(f':MEAS:AMSource {src_list}')
        return

    @property
    def setup_max(self) -> int:
        '''
        Set or query the upper limit of the threshold
        (expressed in the percentage of amplitude) 
        in time, delay, and phase measurements.

        <value> Integer 7 to 95 (default 90)
        '''
        return self.visa.query(f':MEAS:SETup:MAX?')
    @setup_max.setter
    def setup_max(self, upper_limit:int):
        if upper_limit < 7:
            upper_limit = 7 
        if upper_limit > 95:
            upper_limit = 95 
        self.visa.write(f':MEAS:SETup:MAX {upper_limit}')
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
        return self.visa.query(f':MEAS:SETup:MID?')
    @setup_mid.setter
    def setup_mid(self, midpoint:int):
        if midpoint < 6:
            midpoint = 6 
        if midpoint > 94:
            midpoint = 94 
        self.visa.write(f':MEAS:SETup:MID {midpoint}')
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
        return self.visa.query(f':MEAS:SETup:MIN?')
    @setup_min.setter
    def setup_min(self, lower_limit:int):
        if lower_limit < 5:
            lower_limit = 5 
        if lower_limit > 93:
            lower_limit = 93 
        self.visa.write(f':MEAS:SETup:MIN {lower_limit}')
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
        return self.visa.query(f':MEAS:SETup:PSA?')
    @setup_psa.setter
    def setup_psa(self, source:MeasureSources):
        s = source.value
        self.visa.write(f':MEAS:SETup:PSA {s}')
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
        return self.visa.query(f':MEAS:SETup:PSB?')
    @setup_psb.setter
    def setup_psb(self, source:MeasureSources):
        s = source.value
        self.visa.write(f':MEAS:SETup:PSB {s}')
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
        return self.visa.query(f':MEAS:SETup:DSA?')
    @setup_dsa.setter
    def setup_dsa(self, source:MeasureSources):
        s = source.value
        self.visa.write(f':MEAS:SETup:DSA {s}')
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
        return self.visa.query(f':MEAS:SETup:DSB?')
    @setup_dsa.setter
    def setup_dsa(self, source:MeasureSources):
        s = source.value
        self.visa.write(f':MEAS:SETup:DSB {s}')
        return
    

    @property
    def statistic_display(self) -> str:
        '''
        Enable or disable the statistic function, 
        or query the status of the statistic function. 
        
        <bool> Bool {{1|ON}|{0|OFF}} 0|OFF
        '''
        return self.visa.query(f':MEAS:STATistic:DISPlay?')
    @statistic_display.setter
    def statistic_display(self, display_on:bool):
        disp_on = 1 if display_on else 0
        self.visa.write(f':MEAS:STATistic:DISPlay {disp_on}')
        return

    @property
    def statistic_display(self) -> str:
        '''
        Set or query the statistic mode. 
        
        <mode> Discrete {DIFFerence|EXTRemum} (Default EXTRem)
        '''
        return self.visa.query(f':MEAS:STATistic:MODE?')
    @statistic_display.setter
    def statistic_display(self, mode:str):
        self.visa.write(f':MEAS:STATistic:MODE {mode}')
        return

    @property
    def statistic_reset(self) -> str:
        '''
        Clear the history data and make statistic again.
        
        <mode> Discrete {DIFFerence|EXTRemum} (Default EXTRem)
        '''
    def statistic_reset(self):
        self.visa.write(f':MEAS:STATistic:RESet')
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
        return self.visa.query(f':MEAS:STATistic:MODE?')
    @statistic_item.setter
    def statistic_item(self, item:str):
        self.visa.write(f':MEAS:STATistic:MODE {item}')
        return

    # :MEAS:ITEM does not lend itself to get/set methods
    # because both get and set require two parameters
    def item_get(self, item, source='') -> str:
        '''
        Measure any waveform parameter of the specified source, 
        or query the measurement result of any waveform 
        parameter of the specified source;
        If source is ommitted, current :MEAS:SOURCE will be used
        
        <item> Discrete
        {VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|
        VRMS|OVERshoot|PREShoot|MARea|MPARea|
        PERiod|FREQuency|RTIMe|FTIMe|PWIDth|
        NWIDth|PDUTy|NDUTy|RDELay|FDELay|
        RPHase|FPHase|TVMAX|TVMIN|PSLEWrate|
        NSLEWrate|VUPper|VMID|VLOWer|VARIance|
        PVRMS|PPULses|NPULses|PEDGes|NEDGes}

        example:
        :MEASure:ITEM OVERshoot,CHANnel2 // enable overshoot meas on chan2
        :MEASure:ITEM? OVERshoot,CHANnel2
        '''
        cmd_str = f':MEAS:ITEM? {item}'
        if source:
            cmd_str += f",{source}"
        return float(self.visa.query(cmd_str))
    def item_set(self, item:Measurements, source:MeasureSources=''):
        # implementation here is limited to one source;
        # though technically you can specify comma-separated list of sources
        # if len(sources) > 1: 
        #     for source in sources:
        #         item += "," + source
        cmd_str = f':MEAS:ITEM? {item}'
        if source:
            cmd_str += f",{source}"
        self.visa.write(f':MEAS:ITEM {item},{source}')
        return

    # ===== shortcut helpers =====
    def vrms(self, source:MeasureSources):
        return self.item_get(Measurements.VRMS, source=source)
    
    def vmin(self, source:MeasureSources):
        return self.item_get(Measurements.VMIN, source=source)
    
    def vmax(self, source:MeasureSources):
        return self.item_get(Measurements.VMAX, source=source)

    def vavg(self, source:MeasureSources):
        return self.item_get(Measurements.VAVG, source=source)
    
    def vamp(self, source:MeasureSources):
        return self.item_get(Measurements.VAMP, source=source)
    
    def vpp(self, source:MeasureSources):
        return self.item_get(Measurements.VPP, source=source)
    
    def frequency(self, source:MeasureSources):
        return self.item_get(Measurements.FREQUENCY, source=source)
    
    def period(self, source:MeasureSources):
        return self.item_get(Measurements.PERIOD, source=source)