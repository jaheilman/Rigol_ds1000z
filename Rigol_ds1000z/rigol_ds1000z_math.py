from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import OnOff, MathOperations, MathSources, LogicSources, \
    AnalogSources, FFTWindows, FFTUnits, FFTMode, FFTSources, FxOperations
import math

class Rigol_ds1000z_Math:
    '''
    The :MATH commands are used to set the operations between the waveforms of multiple channels.
    Note:  The operations include the following types:
        Algebraic Operations: A+B, A-B, AxB, A/B
        Spectrum Operation: FFT
        Logic Operations: A&&B, A||B, A^B, !A
        Functional Operations: Intg, Diff, Sqrt, Lg, Ln, Exp, Abs
        Filter: Low Pass Filter, High Pass Filter, Band Pass Filter, Band Stop Filter
        Compound Operations: Combination of two operations (inner and outer)
    
    For logic operations, the waveform data to be operated is compared with the preset threshold and is
    converted to 0 or 1. Thus, the result will also be 0 or 1.
    
    For a relatively complicated operation, you can split it into inner and outer layer operations (namely
    compound operation) according to your need. The inner layer operation (fx) can only be algebraic
    operation and the outer layer operation can only be algebraic operation or functional operation.
    
    When the outer layer operation is algeriac operation, at least one of source A and source B of the outer
    layer operation should be set to FX.
    
    When the outer layer operation is functional operation, the source of the outer layer operation can only
    be set to FX.
'''
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)
        self.fft = self.FFT(self.visa)

    @property
    def display(self) -> OnOff:
        '''
        :MATH:DISPlay
        Enable or disable the math operation function or query the math operation status.
        '''
        return int(self.visa.query(':MATH:DISPlay?'))
    @display.setter
    def display(self, display_on_off:OnOff):
        self.visa.write(f':MATH:DISPlay {display_on_off}')
        return

    @property
    def operation(self) -> MathOperations:
        '''
        :MATH:OPERator
        Set or query the operator of the math operation.

        When the parameter in :MATH:SOURce1 and/or :MATH:SOURce2 is FX, this command is
        used to set the operator of the outer layer operation of compound operation.

        <oper> see Constants - MathOperations
        '''
        return (self.visa.query(':MATH:DISPlay?'))
    @operation.setter
    def operation(self, operator:MathOperations):
        self.visa.write(f':MATH:DISPlay {operator}')
        return
    
    @property
    def source_A(self) -> MathSources:
        '''
        :MATH:SOURce1
        Set or query the source or source A of algebraic operation/functional operation/the outer
        layer operation of compound operation.

        <source> {CHANnel1|CHANnel2|CHANnel3|CHANnel4|FX}

        For algebraic operations, this command is used to set source A.
        For functional operations, only this command is used to set the source.
        For compound operations, this command is used to set source A of the outer layer
        operation when the outer layer operation is algeriac operation and the range of
        <src> is {CHANnel1|CHANnel2|CHANnel3|CHANnel4}; this command is used to set
        the source of the outer layer operation when the outer layer operation is functional
        operation and <src> can only be FX.
        Note: When the outer layer operation of compound operation is algebraic operation, at least
        one of source A and source B of the outer layer operation should be set to FX.

        When "FX" is selected, you can send
        the :MATH:OPTion:FX:SOURce1, :MATH:OPTion:FX:SOURce2,
        and :MATH:OPTion:FX:OPERator commands to set the sources and operator of the
        inner layer operation.
        '''
        return (self.visa.query(':MATH:SOURce1?'))
    @source_A.setter
    def source_A(self, source:MathSources):
        self.visa.write(f':MATH:SOURce1 {source}')
        return
    
    @property
    def source_B(self) -> MathSources:
        '''
        :MATH:SOURce2
        Set or query the source or source B of algebraic operation/functional operation/the outer
        layer operation of compound operation.

        <source> {CHANnel1|CHANnel2|CHANnel3|CHANnel4|FX}

        For algebraic operations, this command is used to set source B.
        For functional operations, only this command is used to set the source.
        For compound operations, this command is used to set source B of the outer layer
        operation when the outer layer operation is algebriac operation; 
        when the outer layer operation is functional operation and <src> can only be FX.

        Note: When the outer layer operation of compound operation is algebraic operation, at least
        one of source A and source B of the outer layer operation should be set to FX.

        When "FX" is selected, you can send
        the :MATH:OPTion:FX:SOURce1, :MATH:OPTion:FX:SOURce2,
        and :MATH:OPTion:FX:OPERator commands to set the sources and operator of the
        inner layer operation.
        '''
        return (self.visa.query(':MATH:SOURce2?'))
    @source_B.setter
    def source_B(self, source:MathSources):
        self.visa.write(f':MATH:SOURce2 {source}')
        return
    
    @property
    def logic_source_A(self) -> LogicSources:
        '''
        :MATH:LSOURce1
        Set or query source A of logic operation.

        The logic operations include A&&B, A||B, A^B, and !A.
        '''
        return (self.visa.query(':MATH:LSOURce1?'))
    @logic_source_A.setter
    def logic_source_A(self, source:LogicSources):
        self.visa.write(f':MATH:LSOURce1 {source}')
        return
    
    @property
    def logic_source_B(self) -> LogicSources:
        '''
        :MATH:LSOURce2
        Set or query source B of logic operation.

        The logic operations include A&&B, A||B, A^B, and !A.

        This command is only applicable to logic operations that require two signal sources
        and is used to set source B.
        '''
        return (self.visa.query(':MATH:LSOURce2?'))
    @logic_source_B.setter
    def logic_source_B(self, source:LogicSources):
        self.visa.write(f':MATH:LSOURce2 {source}')
        return
    
    @property
    def scale(self) -> float:
        '''
        :MATH:SCALe
        Set or query the vertical scale of the operation result. The unit depends on the operator
        currently selected and the unit of the source.

        The max range is from 1p to 5T (in 1-2-5 step) Default: 1.00V

        The range of the vertical scale is related to the operator currently selected and the vertical
        scale of the source channel. For the integration (intg) and differential (diff) operations, it
        is also related to the current horizontal timebase.
        '''
        return float(self.visa.query(':MATH:SCALe?'))
    @scale.setter
    def scale(self, scale:float):
        self.visa.write(f':MATH:SCALe {scale}')
        return
    
    @property
    def offset(self) -> float:
        '''
        :MATH:OFFSet
        Set or query the vertical offset of the operation result. The unit depends on the operator
        currently selected and the unit of the source.

        Related to the vertical scale of the operation result
            Range: (-1000 x MathVerticalScale) to (1000 x MathVerticalScale)
            Step: MathVerticalScale/50
        '''
        return float(self.visa.query(':MATH:OFFSet?'))
    @offset.setter
    def offset(self, offset:float):
        self.visa.write(f':MATH:OFFSet {offset}')
        return
    

    @property
    def invert(self) -> OnOff:
        '''
        :MATH:INVert
        Enable or disable the inverted display mode of the operation result, or query the inverted
        display mode status of the operation result.
        '''
        return int(self.visa.query(':MATH:INVert?'))
    @invert.setter
    def invert(self, invert:OnOff):
        self.visa.write(f':MATH:INVert {invert}')
        return
    
    def reset(self):
        '''
        :MATH:RESet
        Sending this command, the instrument adjusts the vertical scale of the operation result to
        the most proper value according to the current operator and the horizontal timebase of
        the source.
        '''
        self.visa.write(f':MATH:RESET')
        return
    
    class FFT:
        def __init__(self, visa:Rigol_visa):
            self.visa = visa
            
        @property
        def source(self) -> FFTSources:
            '''
            :MATH:FFT:SOURce
            Set or query the source of FFT operation/filter.
            '''
            return (self.visa.query(':MATH:FFT:SOURCE?'))
        @source.setter
        def source(self, chan:FFTSources):
            self.visa.write(f':MATH:FFT:SOURCE {chan}')
            return
    
        @property
        def window(self) -> FFTWindows:
            '''
            :MATH:FFT:WINDow
            Set or query the source of FFT operation/filter.
            '''
            return (self.visa.query(':MATH:FFT:WINDow?'))
        @window.setter
        def window(self, window_filter:FFTWindows):
            self.visa.write(f':MATH:FFT:WINDow {window_filter}')
            return
            
        @property
        def split_display(self) -> OnOff:
            '''
            :MATH:FFT:SPLit
            Set or query the source of FFT operation/filter.
            '''
            return int(self.visa.query(':MATH:FFT:SPLit?'))
        @split_display.setter
        def split_display(self, half_screen:OnOff):
            self.visa.write(f':MATH:FFT:SPLit {half_screen}')
            return
        
        @property
        def units(self) -> FFTUnits:
            '''
            :MATH:FFT:UNIT
            Set or query the vertical unit of the FFT operation result.
            '''
            return (self.visa.query(':MATH:FFT:UNIT?'))
        @units.setter
        def units(self, units:FFTUnits):
            self.visa.write(f':MATH:FFT:UNIT {units}')
            return
        
        @property
        def horizontal_scale(self) -> float:
            '''
            :MATH:FFT:HSCale
            <scale> can be set to 1/1000, 1/400, 1/200, 1/100, 1/40, or 1/20 of the FFT sample rate.
            
            When the FFT mode is set to TRACe, FFT sample rate equals to screen sample rate,
            that is, 100/horizontal timebase.
            
            When the FFT mode is set to MEMory, FFT sample rate equals to memory sample
            rate (:ACQuire:SRATe?).
            
            You can view the detailed information of the frequency spectrum by reducing the
            horizontal scale.
            '''
            return float(self.visa.query(':MATH:FFT:HSCale?'))
        @horizontal_scale.setter
        def horizontal_scale(self, scale:float):
            self.visa.write(f':MATH:FFT:HSCale {scale}')
            return
  
        @property
        def horizontal_center(self) -> float:
            '''
            :MATH:FFT:HCENter
            <center> Set or query the center frequency of the FFT operation result, namely the frequency
            relative to the horizontal center of the screen. The default 5MHz.

            When the FFT mode is set to TRACe, the range of <cent> is from 0 to (0.4 x FFT
            sample rate). Wherein, FFT sample rate equals to screen sample rate, that is,
            100/horizontal timebase.

            When the FFT mode is set to MEMory, the range of <cent> is from 0 to (0.5 x FFT
            sample rate). Wherein, FFT sample rate equals to memory sample rate
            (:ACQuire:SRATe?).

            Step = Horizontal Scale of the FFT operation result/50.
            '''
            return float(self.visa.query(':MATH:FFT:HCENter?'))
        @horizontal_center.setter
        def horizontal_center(self, center:float):
            self.visa.write(f':MATH:FFT:HCENter {center}')
            return
        
        @property
        def horizontal_scale(self) -> float:
            '''
            :MATH:FFT:HSCale
            <scale> can be set to 1/1000, 1/400, 1/200, 1/100, 1/40, or 1/20 of the FFT sample rate.
            
            When the FFT mode is set to TRACe, FFT sample rate equals to screen sample rate,
            that is, 100/horizontal timebase.
            
            When the FFT mode is set to MEMory, FFT sample rate equals to memory sample
            rate (:ACQuire:SRATe?).
            
            You can view the detailed information of the frequency spectrum by reducing the
            horizontal scale.
            '''
            return float(self.visa.query(':MATH:FFT:HSCale?'))
        @horizontal_scale.setter
        def horizontal_scale(self, scale:float):
            self.visa.write(f':MATH:FFT:HSCale {scale}')
            return
  
        @property
        def horizontal_mode(self) -> FFTMode:
            '''
            :MATH:FFT:MODE <mode>
            Set or Query the FFT Mode

            TRACe: denotes that the data source of the FFT operation is the data of the
            waveform displayed on the screen.
            
            MEMory: denotes that the data source of the FFT operation is the data of the
            waveform in the memory.
            '''
            return (self.visa.query(':MATH:FFT:MODE?'))
        @horizontal_mode.setter
        def horizontal_mode(self, mode:FFTMode):
            self.visa.write(f':MATH:FFT:MODE {mode}')
            return
        
    class Option:
        def __init__(self, visa:Rigol_visa):
            self.visa = visa

        @property
        def start_point(self) -> int:
            '''
            :MATH:OPTion:STARt
            Set or query the start point of the waveform math operation.

            Range is 0 to endPoint-1.  The source selected is equally divided into 1200 parts 
            horizontally, in which the leftmost is 0 and the rightmost is 1199.
            
            Invalid for FFT.
            '''
            return int(self.visa.query(':MATH:OPTion:STARt?'))
        @start_point.setter
        def start_point(self, start_pt:int):
            self.visa.write(f':MATH:OPTion:STARt {start_pt}')
            return
    
        @property
        def end_point(self) -> int:
            '''
            :MATH:OPTion:END
            Set or query the end point of the waveform math operation.

            Range is startPoint+1 to 1199.  The source selected is equally divided into 1200 parts 
            horizontally, in which the leftmost is 0 and the rightmost is 1199.
            
            Invalid for FFT.
            '''
            return int(self.visa.query(':MATH:OPTion:END?'))
        @end_point.setter
        def end_point(self, end_pt:int):
            self.visa.write(f':MATH:OPTion:END {end_pt}')
            return
        
        @property
        def invert(self) -> OnOff:
            '''
            :MATH:OPTion:INVert
            Enable or disable the inverted display mode of the operation result, 
            or query the inverted display mode status of the operation result.
            '''
            return int(self.visa.query(':MATH:OPTion:END?'))
        @invert.setter
        def invert(self, invert:OnOff):
            self.visa.write(f':MATH:OPTion:END {invert}')
            return
        
        @property
        def vscale_logic(self) -> float:
            '''
            :MATH:OPTion:SENSitivity
            Set or query the sensitivity of the logic operation. The default unit is div (namely the
            current vertical scale).

            This command is only applicable to logic operations (A&&B, A||B, A^B, and !A)
            '''
            return float(self.visa.query(':MATH:OPTion:SENSitivity?'))
        @vscale_logic.setter
        def vscale_logic(self, vertical_scale:float):
            vertical_scale = math.ceil(vertical_scale/0.08)
            self.visa.write(f':MATH:OPTion:SENSitivity {vertical_scale}')
            return
        
        
        @property
        def diff_smoothing_window(self) -> int:
            '''
            :MATH:OPTion:DIStance
            Set or query the smoothing window width of differentiation operation (diff).

            Range is 3 to 201

            This command is only applicable to differentiation operation (diff).
            '''
            return int(self.visa.query(':MATH:OPTion:DIStance?'))
        @diff_smoothing_window.setter
        def diff_smoothing_window(self, window:int):
            if window < 3: window = 3
            if window > 201: window = 201
            self.visa.write(f':MATH:OPTion:DIStance {window}')
            return
            
        @property
        def autoscale(self) -> OnOff:
            '''
            :MATH:OPTion:ASCale
            Enable or disable the auto scale setting of the operation result or query the status of the
            auto scale setting.
            '''
            return int(self.visa.query(':MATH:OPTion:ASCale?'))
        @autoscale.setter
        def autoscale(self, autoscaling:OnOff):
            self.visa.write(f':MATH:OPTion:ASCale {autoscaling}')
            return
        
                
        @property
        def threshold_A(self) -> float:
            '''
            :MATH:OPTion:THReshold1
            Set or query the threshold level of source A in logic operations. The default unit is V.

            (-4 x VerticalScale - VerticalOffset) to
            ( 4 x VerticalScale - VerticalOffset)
            The step is VerticalScale/50
            '''
            return float(self.visa.query(':MATH:OPTion:THReshold1?'))
        @threshold_A.setter
        def threshold_A(self, threshold:float):
            self.visa.write(f':MATH:OPTion:THReshold1 {threshold}')
            return
                        
        @property
        def threshold_B(self) -> float:
            '''
            :MATH:OPTion:THReshold2
            Set or query the threshold level of source A in logic operations. The default unit is V.

            (-4 x VerticalScale - VerticalOffset) to
            ( 4 x VerticalScale - VerticalOffset)
            The step is VerticalScale/50
            '''
            return float(self.visa.query(':MATH:OPTion:THReshold2?'))
        @threshold_B.setter
        def threshold_B(self, threshold:float):
            self.visa.write(f':MATH:OPTion:THReshold2 {threshold}')
            return

        @property
        def fx_source_A(self) -> AnalogSources:
            '''
            :MATH:OPTion:FX:SOURce1
            Set or query source A of the inner layer operation of compound operation.

            <source> {CHANnel1|CHANnel2|CHANnel3|CHANnel4}
            '''
            return float(self.visa.query(':MATH:OPTion:FX:SOURce1?'))
        @fx_source_A.setter
        def fx_source_A(self, source:AnalogSources):
            self.visa.write(f':MATH:OPTion:FX:SOURce1 {source}')
            return
        
        @property
        def fx_source_B(self) -> AnalogSources:
            '''
            :MATH:OPTion:FX:SOURce2
            Set or query source B of the inner layer operation of compound operation.

            <source> {CHANnel1|CHANnel2|CHANnel3|CHANnel4}
            '''
            return float(self.visa.query(':MATH:OPTion:FX:SOURce2?'))
        @fx_source_B.setter
        def fx_source_B(self, source:AnalogSources):
            self.visa.write(f':MATH:OPTion:FX:SOURce2 {source}')
            return
        
        
        @property
        def fx_operator(self) -> FxOperations:
            '''
            :MATH:OPTion:FX:OPERator
            et or query the operator of the inner layer operation of compound operation.

            <op> {ADD|SUBTract|MULTiply|DIVision}
            '''
            return float(self.visa.query(':MATH:OPTion:FX:SOURce2?'))
        @fx_operator.setter
        def fx_operator(self, op:FxOperations):
            self.visa.write(f':MATH:OPTion:FX:SOURce2 {op}')
            return

