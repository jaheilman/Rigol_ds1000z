from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import DecoderMode, DecoderFormat, DecoderUart, UartParity

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
    def threshold_auto(self, enable:float):
        en = 1 if enable else 0 
        self.visa.write(f':DECoder{self._decoder}:THREshold:AUTO {en}')
        return
    
    @property
    def config_label(self) -> bool:
        '''
        Turn on or off the label display function, or query the status of the label display function.
        '''
        en = (self.visa.query(f':DECoder{self._decoder}:CONFig:LABel?'))
        enabled = True if en == 1 else False
        return enabled
    @config_label.setter
    def config_label(self, enable:bool):
        en = 1 if enable else 0 
        self.visa.write(f':DECoder{self._decoder}:CONFig:LABel {en}')
        return
    
    @property
    def config_line(self) -> bool:
        '''
        Turn on or off the label display function, or query the status of the label display function.

        When this function is enabled, the bus will be displayed on the screen. You can send
        the :DECoder<n>:POSition command to adjust the vertical display position of the bus.
        '''
        en = (self.visa.query(f':DECoder{self._decoder}:CONFig:LINE?'))
        enabled = True if en == 1 else False
        return enabled
    @config_line.setter
    def config_line(self, enable:bool):
        en = 1 if enable else 0 
        self.visa.write(f':DECoder{self._decoder}:CONFig:LINE {en}')
        return
    
    @property
    def config_format(self) -> bool:
        '''
        Turn on or off the format display function, or query the status of the format display function.

        When this function is turned on, the current bus display format will be displayed at the
        right of the label display (when the bus display is turned on). You can send
        the :DECoder<n>:FORMat command to set the bus display format.
        '''
        en = (self.visa.query(f':DECoder{self._decoder}:CONFig:FORMAT?'))
        enabled = True if en == 1 else False
        return enabled
    @config_format.setter
    def config_format(self, enable:bool):
        en = 1 if enable else 0 
        self.visa.write(f':DECoder{self._decoder}:CONFig:FORMAT {en}')
        return
    
   
    @property
    def config_endian(self) -> bool:
        '''
        Turn on or off the endian display function in serial bus decoding, or query the status of
        the endian display function in serial bus decoding.
        '''
        en = (self.visa.query(f':DECoder{self._decoder}:CONFig:ENDIan?'))
        enabled = True if en == 1 else False
        return enabled
    @config_endian.setter
    def config_endian(self, enable:bool):
        en = 1 if enable else 0 
        self.visa.write(f':DECoder{self._decoder}:CONFig:ENDIan {en}')
        return
    
    @property
    def config_endian(self) -> bool:
        '''
        Turn on or off the endian display function in serial bus decoding, or query the status of
        the endian display function in serial bus decoding.

        When this function is enabled, the current bus endian will be displayed at the right of
        the format display (when the bus display is turned on).

        This command is invalid in parallel decoding.
        '''
        en = (self.visa.query(f':DECoder{self._decoder}:CONFig:ENDIan?'))
        enabled = True if en == 1 else False
        return enabled
    @config_endian.setter
    def config_endian(self, enable:bool):
        en = 1 if enable else 0 
        self.visa.write(f':DECoder{self._decoder}:CONFig:ENDIan {en}')
        return
    
    @property
    def config_width(self) -> bool:
        '''
        Turn on or off the width display function, or query the status of the width display function.

        When this function is enabled, the width of each frame of data will be displayed at the
        right of the endian display (when the bus display is turned on).   
        '''
        en = (self.visa.query(f':DECoder{self._decoder}:CONFig:WIDth?'))
        enabled = True if en == 1 else False
        return enabled
    @config_width.setter
    def config_width(self, enable:bool):
        en = 1 if enable else 0 
        self.visa.write(f':DECoder{self._decoder}:CONFig:WIDth {en}')
        return
    

    @property
    def config_samplerate(self) -> float:
        '''
        Query the current digital sample rate.  

        The digital sample rate is related to the data source currently selected. By default, the
        data source is "Trace"; at this point, the digital sample rate is related to the horizontal
        time base. 
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:CONFig:SRATe?'))
    
    @property
    def uart_tx(self) -> str:
        '''
        Set or query the TX channel source of RS232 decoding. 

        When OFF is selected, no TX channel source will be set. The TX channel source and RX
        channel source (:DECoder<n>:UART:RX) cannot be both set to OFF.  
        '''
        return (self.visa.query(f':DECoder{self._decoder}:UART:TX?'))
    @uart_tx.setter
    def uart_tx(self, channel:DecoderUart):
        self.visa.write(f':DECoder{self._decoder}:UART:TX {channel}')
        return
    
    @property
    def uart_rx(self) -> str:
        '''
        Set or query the RX channel source of RS232 decoding. 

        When OFF is selected, no RX channel source will be set. The RX channel source and TX
        channel source (:DECoder<n>:UART:TX) cannot be both set to OFF.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:UART:RX?'))
    @uart_rx.setter
    def uart_rx(self, channel:DecoderUart):
        self.visa.write(f':DECoder{self._decoder}:UART:RX {channel}')
        return
    
    
    @property
    def uart_polarity(self) -> str:
        '''
        Set or query the polarity of RS232 decoding.

        POSITIVE polarity high is 1 and low is 0.
        NEGATIVE polarity high is 0 and low is 1.  
        '''
        return (self.visa.query(f':DECoder{self._decoder}:UART:POLarity?'))
    @uart_polarity.setter
    def uart_polarity(self, positive_polarity:bool):
        pol = 1 if positive_polarity else 0
        self.visa.write(f':DECoder{self._decoder}:UART:POLarity {pol}')
        return

   
    @property
    def uart_endian(self) -> str:
        '''
        Set or query the endian of RS232 decoding.  
        '''
        return (self.visa.query(f':DECoder{self._decoder}:UART:ENDIan?'))
    @uart_polarity.setter
    def uart_polarity(self, lsb_endian:bool):
        endian = "LSB" if lsb_endian else "MSB"
        self.visa.write(f':DECoder{self._decoder}:UART:ENDIan {endian}')
        return
    

    @property
    def uart_baud(self) -> int:
        '''
        Set or query the buad rate of RS232 decoding. The default unit is bps (baud per second).

        The query returns the current baud rate in integer.  

        Baud rate must be <int> between 110 and 20M.  Default 9600
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:UART:BAUD?'))
    @uart_baud.setter
    def uart_baud(self, baud_rate:int):
        if (baud_rate < 110): baud_rate = 110
        if (baud_rate > 20000000): baud_rate = 20000000
        self.visa.write(f':DECoder{self._decoder}:UART:BAUD {baud_rate}')
        return
    
    @property
    def uart_width(self) -> int:
        '''
        Set or query the width of each frame of data in RS232 decoding.

        Width is an integer between 5 and 8; default 8.
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:UART:WIDth?'))
    @uart_width.setter
    def uart_width(self, frame_width:int):
        if (frame_width < 5): frame_width = 5
        if (frame_width > 8): frame_width = 8
        self.visa.write(f':DECoder{self._decoder}:UART:WIDth {frame_width}')
        return
    
    
    @property
    def uart_stop_bit(self) -> float:
        '''
        Set or query the stop bit after each frame of data in RS232 decoding.

        stop_bit is 1, 1.5, or 2; Default 1.
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:UART:STOP?'))
    @uart_stop_bit.setter
    def uart_stop_bit(self, stop_bit:float):
        assert stop_bit in [1, 1.5, 2]
        self.visa.write(f':DECoder{self._decoder}:UART:STOP {stop_bit}')
        return
    
    @property
    def uart_parity(self) -> str:
        '''
        Set or query the even-odd check mode of the data transmission in RS232 decoding.

        Parity is {NONE|EVEN|ODD}; Default NONE
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:UART:PARity?'))
    @uart_parity.setter
    def uart_parity(self, parity:UartParity):
        self.visa.write(f':DECoder{self._decoder}:UART:PARity {parity}')
        return