from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import DecoderMode, DecoderFormat

class Rigol_ds1000z_Decoder:
    def __init__(self, visa_resource, n_decoder):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)
        self._decoder = n_decoder

    @property
    def mode(self) -> str:
        '''
        Set or query the decoder type for decoder 1

        <mode> Discrete {PARallel|UART|SPI|IIC} PARallel
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:MODE?'))
    @mode.setter
    def mode(self, mode:DecoderMode):
        self.visa.write(f':DECoder{self._decoder}:MODE {mode}')
        return
    
    @property
    def display(self) -> int:
        '''
        Turn on or off the decoder or query the status of the decoder.

        <enable> bool true = enabled, false = disabled

        returns 1 if enabled, 0 if disabled
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:DISPlay?'))
    @display.setter
    def display(self, enable:bool):
        en = 1 if enable else 0
        self.visa.write(f':DECoder{self._decoder}:DISPlay {en}')
        return
    
  
    @property
    def format(self) -> str:
        '''
        Set or query the bus display format.

        <fmt> Discrete {HEX|ASCii|DEC|BIN|LINE} default ASCII
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:FORMat?'))
    @format.setter
    def format(self, format:DecoderFormat):
        self.visa.write(f':DECoder{self._decoder}:FORMat {format}')
        return
    
  
    @property
    def position(self) -> str:
        '''
        Set or query the vertical position of the bus on the screen.

        <pos> Integer 50 to 350  default Decoder 1: 350
                                         Decoder 2: 300
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:POSition?'))
    @position.setter
    def position(self, pos:int):
        if pos < 50: pos = 50
        if pos > 350: pos = 350
        self.visa.write(f':DECoder{self._decoder}:POSition {pos}')
        return
    
    @property
    def threshold_chan1(self) -> float:
        '''
        Set or query the threshold level of the specified analog channel.

        <thresh> Real (-4 x VerticalScale - VerticalOffset) to
                      (4 x VerticalScale - VerticalOffset)
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel1?'))
    @threshold_chan1.setter
    def threshold_chan1(self, thresh:float):
        chan = 1
        thresh = self._verify_threshold(chan, thresh) 
        self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {thresh}')
        return
    
    @property
    def threshold_chan2(self) -> float:
        '''
        Set or query the threshold level of the specified analog channel.

        <thresh> Real (-4 x VerticalScale - VerticalOffset) to
                      (4 x VerticalScale - VerticalOffset)
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel2?'))
    @threshold_chan2.setter
    def threshold_chan2(self, thresh:float):
        chan = 2
        thresh = self._verify_threshold(chan, thresh)
        self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {thresh}')
        return
    
    @property
    def threshold_chan3(self) -> float:
        '''
        Set or query the threshold level of the specified analog channel.

        <thresh> Real (-4 x VerticalScale - VerticalOffset) to
                      (4 x VerticalScale - VerticalOffset)
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel3?'))
    @threshold_chan3.setter
    def threshold_chan1(self, thresh:float):
        chan = 3
        thresh = self._verify_threshold(chan, thresh)
        self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {thresh}')
        return
     
    @property
    def threshold_chan4(self) -> float:
        '''
        Set or query the threshold level of the specified analog channel.

        <thresh> Real (-4 x VerticalScale - VerticalOffset) to
                      (4 x VerticalScale - VerticalOffset)
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel4?'))
    @threshold_chan4.setter
    def threshold_chan4(self, thresh:float):
        chan = 4
        thresh = self._verify_threshold(chan, thresh) 
        self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {thresh}')
        return
    
    def _verify_threshold(self, chan, thresh):
        v_scale = self.visa.query(f":CHAN{chan}:SCALe?")
        v_offset = self.visa.query(f":CHAN{chan}:OFFSet?")
        if thresh < (-4*v_scale - v_offset): thresh = (-4*v_scale - v_offset)
        if thresh > ( 4*v_scale + v_offset): thresh = ( 4*v_scale + v_offset) 
        return thresh
    
     
    @property
    def threshold_auto(self) -> bool:
        '''
        Turn on or off the auto threshold function of the analog channels, or query the status of
        the auto threshold function of the analog channels.
        '''
        en = (self.visa.query(f':DECoder{self._decoder}:THREshold:AUTO?'))
        auto_enabled = True if en == 1 else False
        return auto_enabled
    @threshold_auto.setter
    def threshold_auto(self, enable_auto:float):
        en = 1 if enable_auto else 0 
        self.visa.write(f':DECoder{self._decoder}:THREshold:AUTO {en}')
        return