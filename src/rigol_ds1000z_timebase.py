from rigol_visa import Rigol_visa

class Rigol_ds1000z_Timebase:
    '''
    The :TIMebase commands are used to set the 
    horizontal parameters, such as enabling the delayed
    sweep and setting the horizontal timebase mode.
    '''
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)


    @property
    def delay_enable(self) -> bool:
        '''
        Enable or disable the delayed sweep, or query the status of the delayed sweep.
        
        <enable> Bool {{1|ON}|{0|OFF}}  default 0 
        '''
        return self.visa.query(f':TIMebase:DELay:ENABle?')
    @delay_enable.setter
    def delay_enable(self, enable:bool):
        en = 1 if enable else 0
        self.visa.write(f':TIMebase:DELay:ENABle {en}')
        return
    
    @property
    def delay_offset(self) -> float:
        '''
        Set or query the delayed timebase offset. The default unit is s.

        <offset> Float -(LeftTime - DelayRange/2) to
                        (RightTime - DelayRange/2)  Default 0
        '''
        return float(self.visa.query(f':TIMebase:DELay:OFFSet?'))
    @delay_offset.setter
    def delay_offset(self, offset:float):
        self.visa.write(f':TIMebase:DELay:OFFSet {offset}')
        return
    
    @property
    def delay_scale(self) -> float:
        '''
        Set or query the delayed timebase scale. The default unit is s/div

        <scale> The maximum value of <scale> is the main 
        timebase scale currently set, and
        the minimum value is expressed as:
        50/(current sample rate x amplification factor)

        See Programmer reference for further detail
        '''
        return float(self.visa.query(f':TIMebase:DELay:SCALe?'))
    @delay_scale.setter
    def delay_scale(self, scale:float):
        self.visa.write(f':TIMebase:DELay:SCALe {scale}')
        return
    
    @property
    def offset(self) -> float:
        '''
        Set or query the main timebase offset. The default unit is s.

        The range of <offset> is related to the current mode of the horizontal
        timebase (refer to :TIMebase:MODE) and run state of the oscilloscope.
        '''
        return float(self.visa.query(f':TIMebase:MAIN:OFFSet?'))
    @offset.setter
    def offset(self, offset:float):
        self.visa.write(f':TIMebase:MAIN:OFFSet {offset}')
        return
    
    @property
    def main_offset(self) -> float:
        '''
        Same as timebase.offset
        '''
        return self.offset
    @main_offset.setter
    def main_offset(self, offset:float):
        self.offset = offset
        return
    
    @property
    def scale(self) -> float:
        '''
        Set or query the main timebase scale. The default unit is s/div

        <scale> 
          Real YT mode: 5ns/div to 50s/div in 1-2-5 step
          Roll mode: 200ms/div to 50s/div in 1-2-5 step 1μs/div
        '''
        return float(self.visa.query(f':TIMebase:MAIN:SCALe?'))
    @scale.setter
    def scale(self, scale:float):
        self.visa.write(f':TIMebase:MAIN:SCALe {scale}')
        return
    
    @property
    def main_scale(self) -> float:
        '''
        Same as timebase.scale
        '''
        return self.scale
    @main_scale.setter
    def main_scale(self, scale:float):
        self.scale = scale
        return
    
    @property
    def mode(self) -> str:
        '''
        Set or query the mode of the horizontal timebase.

        <mode> Discrete {MAIN|XY|ROLL} default MAIN
        '''
        return float(self.visa.query(f':TIMebase:MODE?'))
    @mode.setter
    def mode(self, mode:float):
        self.visa.write(f':TIMebase:MODE {mode}')
        return