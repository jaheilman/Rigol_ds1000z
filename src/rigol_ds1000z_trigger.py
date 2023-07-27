from rigol_visa import Rigol_visa

class _Rigol1000zTrigger:
    '''
    Handles the trigger configuration.
    '''

    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)

    @property
    def mode(self) -> str:
        '''
        Select or query the trigger type.

        <mode> {EDGE|PULSe|RUNT|WIND|NEDG|SLOPe|VIDeo|
                PATTern|DELay|TIMeout|DURation|SHOLd|
                RS232|IIC|SPI}
        '''
        return self.visa_ask(':TRIGger:MODE?')
    @mode.setter
    def mode(self, mode:str):
        self.visa_write(f':TRIGger:MODE {mode}')
        return

    @property
    def coupling(self) -> str:
        '''
        Select or query the trigger coupling type

        <couple> Discrete {AC|DC|LFReject|HFReject} default=DC
        '''
        return self.visa_ask(':TRIGger:COUPling?')
    @coupling.setter
    def coupling(self, mode:str):
        self.visa_write(f':TRIGger:COUPling {mode}')
        return

    @property
    def status(self) -> str:
        return self.visa_ask(f':TRIGger:STATus?')

    @property
    def sweep(self) -> str:
        '''
        Set or query the trigger mode

        <sweep> Discrete {AUTO|NORMal|SINGle} default=AUTO
        '''
        return self.visa_ask(':TRIGger:SWEep?')
    @sweep.setter
    def sweep(self, sweep:str):
        self.visa_write(f':TRIGger:SWEep {sweep}')
        return
    
    @property
    def holdoff(self) -> str:
        '''
        Set or query the trigger holdoff time. The default unit is s.

        <holdoff> float 16ns to 10s default=16ns
        '''
        return self.visa_ask(':TRIGger:HOLDoff?')
    @holdoff.setter
    def holdoff(self, holdoff:float):
        self.visa_write(f':TRIGger:HOLDoff {holdoff}')
        return
    
    @property
    def noise_reject(self) -> bool:
        '''
        Enable or disable noise rejection,
        or query the status of noise rejection

        <bool> Bool {{1|ON}|{0|OFF}} 0|OFF
        '''
        nr = self.visa_ask(':TRIGger:NREJect?')
        nr_bool = True if nr else False
        return nr_bool
    @noise_reject.setter
    def noise_reject(self, nr_enabled:bool):
        nr = 1 if nr_enabled else 0
        self.visa_write(f':TRIGger:NREJect {nr}')
        return
    
    @property
    def position(self) -> int:
        '''
        Query the position in the internal memory that corresponds to the waveform trigger
        position.

        The query returns an integer.
         -2 denotes that the instrument is not triggered and there is no trigger position.
         -1 denotes the instrument is triggered outside the internal memory; namely, at this
        point, users cannot set the instrument to read the data in the internal memory
        starting from the trigger position.
         An integer that is greater than 0 denotes that the return value is the position in the
        internal memory that corresponds to the trigger position

        '''
        nr = self.visa_ask(':TRIGger:POSition?')
        nr_bool = True if nr else False
        return nr_bool

    @property
    def edge_source(self) -> str:
        '''
        Enable or disable noise rejection,
        or query the status of noise rejection

        <source> Discrete
            {D0|D1|D2|D3|D4|D5|D6|D7|D8|
            D9|D10|D11|D12|D13|D14|D15|
            CHANnel1|CHANnel2|CHANnel3|CHANnel4|AC}
            CHANnel1
        '''
        nr = self.visa_ask(':TRIGger:EDGe:SOURce?')
        nr_bool = True if nr else False
        return nr_bool
    @edge_source.setter
    def edge_source(self, source:str):
        self.visa_write(f':TRIGger:EDGe:SOURce {source}')
        return
    
    @property
    def edge_slope(self) -> str:
        '''
        Enable or disable noise rejection,
        or query the status of noise rejection

        <slope> Discrete {POSitive|NEGative|RFALl} default=POSitive
        '''
        return self.visa_ask(':TRIGger:EDGe:SLOPe?')
    @edge_slope.setter
    def edge_slope(self, slope:str):
        self.visa_write(f':TRIGger:EDGe:SLOPe {slope}')
        return
    
    @property
    def edge_level(self) -> float:
        '''
        Set or query the trigger level in edge trigger. 
        The unit is the same as the current
        amplitude unit of the signal source selected

        <level> Real (-5 x VerticalScale - OFFSet) to
                     ( 5 x VerticalScale - OFFSet) 
                     default = 0
        '''
        return self.visa_ask(':TRIGger:EDGe:LEVel?')
    @edge_level.setter
    def edge_level(self, level:str):
        self.visa_write(f':TRIGger:EDGe:LEVel {level}')
        return
    


#  :TRIGger:PULSe:SOURce
#  :TRIGger:PULSe:WHEN
#  :TRIGger:PULSe:WIDTh
#  :TRIGger:PULSe:UWIDth
#  :TRIGger:PULSe:LWIDth
#  :TRIGger:PULSe:LEVe