from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import OnOff, MeasureItems, MeasureSources, Measurements, AnalogChannels, StatisticsMode, MeasureStatisticsType
from typing import List


class Rigol_ds1000z_Measure:
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)
        self.setup = self.Setup(visa_resource)
        self.statistic = self.Statistic(visa_resource)

    @property
    def source(self) -> MeasureSources:
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
    def counter_source(self) -> MeasureSources:
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
    def counter_value(self) -> MeasureItems:
        '''
        Query the measurement result of the frequency counter. The default unit is Hz

        The query returns the measurement result in scientific notation. 
        If the frequency counter is disabled, 0.0000000e+00 will be returned.
        Example -- :MEASure:COUNter:VALue? /*The query returns 1.000004e+03*/
        '''
        return self.visa.query(f':MEAS:COUNter:VALue?')
    
    # # clear and recover don't code well in @property/setter so I'm sticking to a standard method:
    # # mydso.measure.clear('ALL') # seems obvious
    # # mydso.measure.clear = 'ALL' # whaaaat???

    # @property
    # def clear(self):
    #     return
    # @clear.setter
    # def clear(self, item:MeasureItems):
    #     '''
    #     Clear one or all of the last five measurement items enabled
    #     <item> {ITEM1|ITEM2|ITEM3|ITEM4|ITEM5|ALL}
    #     '''
    #     self.visa.write(f':MEAS:CLEar {item}')
    #     return

    def clear(self, item:MeasureItems):
        '''
        Clear one or all of the last five measurement items enabled
        <item> {ITEM1|ITEM2|ITEM3|ITEM4|ITEM5|ALL}
        '''
        self.visa.write(f':MEAS:CLEar {item}')
        return
    
    def recover(self, item:MeasureItems):
        '''
        Recover the measurement item which has been cleared.
        <item> {ITEM1|ITEM2|ITEM3|ITEM4|ITEM5|ALL}
        '''
        self.visa.write(f':MEAS:RECover {item}')
        return

    @property
    def all_display(self) -> OnOff:
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
        return int(self.visa.query(f':MEAS:ADISplay?'))
    @all_display.setter
    def all_display(self, display_all:OnOff):
        self.visa.write(f':MEAS:ADISplay {display_all}')
        return


    @property
    def all_measure_source(self) -> str:
        '''
        Set or query the source(s) of the all measurement function

        <src> Discrete {CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH} 
        '''
        return self.visa.query(f':MEAS:AMSource?')
    @all_measure_source.setter
    def all_measure_source(self, source:AnalogChannels):
        self.visa.write(f':MEAS:AMSource {source}')
        return
    
    @property
    def all_measure_source_list(self) -> str:
        '''
        Set or query the source(s) of the all measurement function

        <src> Discrete {CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH} 
        '''
        return self.visa.query(f':MEAS:AMSource?')
    @all_measure_source_list.setter
    def all_measure_source_list(self, sources:List[AnalogChannels]):
        if type(sources) != list:
            return
        src_list_str = ''
        for source in sources: # make a comma list from the provided sources
            src_list_str += source + ','
        src_list_str = src_list_str[0:-1] # drop trailing comma
        self.visa.write(f':MEAS:AMSource {src_list_str}')
        return

    class Setup:
        def __init__(self, visa_resource):
            self.visa_resource = visa_resource
            self.visa = Rigol_visa(visa_resource)

        @property
        def max_threshold(self) -> int:
            '''
            Set or query the upper limit of the threshold
            (expressed in the percentage of amplitude) 
            in time, delay, and phase measurements.

            <value> Integer 7 to 95 (default 90)
            '''
            return self.visa.query(f':MEAS:SETup:MAX?')
        @max_threshold.setter
        def max_threshold(self, upper_limit:int):
            if upper_limit < 7:
                upper_limit = 7 
            if upper_limit > 95:
                upper_limit = 95 
            self.visa.write(f':MEAS:SETup:MAX {upper_limit}')
            return

        @property
        def mid_threshold(self) -> int:
            '''
            Set or query the middle point of the threshold
            (expressed in the percentage of amplitude)
            in time, delay, and phase measurements.
            
            The middle point must be lower than the upper limit and greater than the lower limit

            <value> Integer 6 to 94 (default 50)
            '''
            return self.visa.query(f':MEAS:SETup:MID?')
        @mid_threshold.setter
        def mid_threshold(self, midpoint:int):
            if midpoint < 6:
                midpoint = 6 
            if midpoint > 94:
                midpoint = 94 
            self.visa.write(f':MEAS:SETup:MID {midpoint}')
            return

        @property
        def min_threshold(self) -> int:
            '''
            Set or query the lower limit of the threshold
            (expressed in the percentage of amplitude)
            in time, delay, and phase measurements.
            
            The middle point must be lower than the upper limit and greater than the lower limit

            <value> Integer 6 to 94 (default 50)
            '''
            return self.visa.query(f':MEAS:SETup:MIN?')
        @min_threshold.setter
        def min_threshold(self, lower_limit:int):
            if lower_limit < 5:
                lower_limit = 5 
            if lower_limit > 93:
                lower_limit = 93 
            self.visa.write(f':MEAS:SETup:MIN {lower_limit}')
            return

        @property
        def phase_source_a(self) -> MeasureSources:
            '''
            Set or query source A of Phase 1→2 and Phase 1→2 measurements.
            
            <source> Discrete
                {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                D9|D10|D11|D12|D13|D14|D15|
                CHANnel1|CHANnel2|CHANnel3|CHANnel4}
            '''
            return self.visa.query(f':MEAS:SETup:PSA?')
        @phase_source_a.setter
        def phase_source_a(self, source:MeasureSources):
            s = source.value
            self.visa.write(f':MEAS:SETup:PSA {s}')
            return

        @property
        def phase_source_b(self) -> MeasureSources:
            '''
            Set or query source B of Phase 1→2 and Phase 1→2 measurements.
            
            <source> Discrete
                {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                D9|D10|D11|D12|D13|D14|D15|
                CHANnel1|CHANnel2|CHANnel3|CHANnel4}
            '''
            return self.visa.query(f':MEAS:SETup:PSB?')
        @phase_source_b.setter
        def phase_source_b(self, source:MeasureSources):
            s = source.value
            self.visa.write(f':MEAS:SETup:PSB {s}')
            return

        @property
        def delay_source_a(self) -> MeasureSources:
            '''
            Set or query source A of Delay 1→2 and Delay 1→2 measurements.
            
            <source> Discrete
                {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                D9|D10|D11|D12|D13|D14|D15|
                CHANnel1|CHANnel2|CHANnel3|CHANnel4}
            '''
            return self.visa.query(f':MEAS:SETup:DSA?')
        @delay_source_a.setter
        def delay_source_a(self, source:MeasureSources):
            s = source.value
            self.visa.write(f':MEAS:SETup:DSA {s}')
            return

        @property
        def delay_source_b(self) -> MeasureSources:
            '''
            Set or query source B of Delay 1→2 and Delay 1→2 measurements.
            
            <source> Discrete
                {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                D9|D10|D11|D12|D13|D14|D15|
                CHANnel1|CHANnel2|CHANnel3|CHANnel4}
            '''
            return self.visa.query(f':MEAS:SETup:DSB?')
        @delay_source_b.setter
        def delay_source_b(self, source:MeasureSources):
            s = source.value
            self.visa.write(f':MEAS:SETup:DSB {s}')
            return
        

    class Statistic:
        def __init__(self, visa_resource):
            self.visa_resource = visa_resource
            self.visa = Rigol_visa(visa_resource)

        @property
        def display(self) -> str:
            '''
            Enable or disable the statistic function, 
            or query the status of the statistic function. 
            
            <bool> Bool {{1|ON}|{0|OFF}} 0|OFF
            '''
            return self.visa.query(f':MEAS:STATistic:DISPlay?')
        @display.setter
        def display(self, display_on:bool):
            disp_on = 1 if display_on else 0
            self.visa.write(f':MEAS:STATistic:DISPlay {disp_on}')
            return

        @property
        def mode(self) -> StatisticsMode:
            '''
            Set or query the statistic mode. 
            
            <mode> Discrete {DIFFerence|EXTRemum} (Default EXTRem)
            '''
            return self.visa.query(f':MEAS:STATistic:MODE?')
        @mode.setter
        def mode(self, mode:StatisticsMode):
            self.visa.write(f':MEAS:STATistic:MODE {mode}')
            return

        def reset(self):
            '''
            Clear the history data and make statistic again.
            '''
            self.visa.write(f':MEAS:STATistic:RESet')
            return


        def item_get(self, type:MeasureStatisticsType, item:Measurements, source:MeasureSources='') -> str:
            '''
            :MEAS:STATistic:ITEM? <type>,<item>[,<src>,<src>,...]
            Query the statistic result
            of any waveform parameter of the specified source.
        
            <type> Discrete {MAXimum|MINimum|CURRent|AVERages|DEViation}
            
            <item> see constants - Measurements
            
            <source> see constants - MeasureSources; can be a single source or comma separated list
            '''
            cmd_str = f':MEAS:STATistic:ITEM? {type},{item}'
            if source:
                cmd_str += f",{source}"
            return str(self.visa.query(cmd_str))
        def item_set(self, item:Measurements, source:MeasureSources=''):
            '''
            :MEAS:STATistic:ITEM <item>[,<src>,<src>,...]
            Enable the statistic function of any waveform parameter 
            of the specified source.
            
            <item> see constants - Measurements
            
            <source> see constants - MeasureSources; can be a single source or comma separated list
            '''
            cmd_str = f':MEAS:STATistic:ITEM {item}'
            if source:
                cmd_str += f",{source}"
            self.visa.write(f'{cmd_str}')
            return

    # :MEAS:ITEM does not lend itself to get/set methods
    # because both get and set require two parameters
    def item_get(self, item:Measurements, source:MeasureSources='') -> str:
        '''
        :MEAS:ITEM[?]
        Measure any waveform parameter of the specified source, or query the 
        measurement result of any waveform parameter of the specified source;
        If source is ommitted, current :MEAS:SOURCE will be used
        
        <item> see constants - Measurements
        
        <source> see constants - MeasureSources; can be a single source or comma separated list

        example:
        :MEASure:ITEM OVERshoot,CHANnel2 // enable overshoot meas on chan2
        :MEASure:ITEM? OVERshoot,CHANnel2
        '''
        cmd_str = f':MEAS:ITEM? {item}'
        if source:
            cmd_str += f",{source}"
        return str(self.visa.query(cmd_str))
    def item_set(self, item:Measurements, source:MeasureSources=''):
        cmd_str = f':MEAS:ITEM {item}'
        if source:
            cmd_str += f",{source}"
        self.visa.write(f'{cmd_str}')
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
    
    def vtop(self, source:MeasureSources):
        return self.item_get(Measurements.VTOP, source=source)
    
    def vbase(self, source:MeasureSources):
        return self.item_get(Measurements.VBASE, source=source)
       
    def vrms_period(self, source:MeasureSources):
        '''
        V_RMS measured for a single period (rather than all of screen)
        '''
        return self.item_get(Measurements.PVRMS, source=source) 

    def frequency(self, source:MeasureSources):
        return self.item_get(Measurements.FREQUENCY, source=source)

    def period(self, source:MeasureSources):
        return self.item_get(Measurements.PERIOD, source=source)

    def overshoot(self, source:MeasureSources):
        '''
        Overshoot: the ratio of the difference of the maximum value and top value of
        the waveform to the amplitude value.
        '''
        return self.item_get(Measurements.OVERSHOOT, source=source)
    
    def preshoot(self, source:MeasureSources):
        '''
        Preshoot: the ratio of the difference of the minimum value and base value of
        the waveform to the amplitude value.
        '''
        return self.item_get(Measurements.PRESHOOT, source=source)
    
    def area(self, source:MeasureSources):
        '''
        The area of the whole waveform within the screen and in units Vs. The
        area of the waveform above the zero reference (namely the vertical offset) is
        positive and the area of the waveform below the zero reference is negative. The
        area measured is the algebraic sum of the area of the whole waveform within
        the screen.
        '''
        return self.item_get(Measurements.MAREA, source=source)
    
    def area_period(self, source:MeasureSources):
        '''
        The area of the first period of waveform on the screen in units Vs. 
        The area of the waveform above the zero reference (namely the vertical
        offset) is positive and the area of the waveform below the zero reference is
        negative. The area measured is the algebraic sum of the area of the whole 
        period waveform.
        '''
        return self.item_get(Measurements.MPAREA, source=source)
    
    def rise_time(self, source:MeasureSources):
        return self.item_get(Measurements.RTIME, source=source)

    def fall_time(self, source:MeasureSources):
        return self.item_get(Measurements.FTIME, source=source)
    