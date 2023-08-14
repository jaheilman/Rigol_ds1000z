from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import class_has_value, OnOff, Polarity, Endianess, \
    DecoderMode, DecoderFormat, DecoderChannel, DecoderEndian, \
    UartParity, UartStopBits, \
    I2CAddressMode, SpiPolarity, SpiEdge, SpiTimeout

class Rigol_ds1000z_Decoder:
    def __init__(self, visa_resource, n_decoder):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)
        self._decoder = n_decoder

    @property
    def mode(self) -> str:
        '''
        :DECODER{0|1}:MODE[?] <mode>
        Set or query the decoder type for decoder 1

        <mode> literal {PARallel|UART|SPI|IIC}; Default: PARallel
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:MODE?'))
    @mode.setter
    def mode(self, mode:DecoderMode):
        self.visa.write(f':DECoder{self._decoder}:MODE {mode}')
        return
    
    @property
    def display(self) -> OnOff:
        '''
        :DECODER{0|1}:DISPLAY[?] <display>
        Turn on or off the decoder or query the status of the decoder.

        <display> bool true = enabled, false = disabled

        returns 1 if enabled, 0 if disabled
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:DISPlay?'))
    @display.setter
    def display(self, display:OnOff):
        self.visa.write(f':DECoder{self._decoder}:DISPlay {display}')
        return
    
  
    @property
    def format(self) -> str:
        '''
        :DECODER{0|1}:FORMAT[?] <format>
        Set or query the bus display format.

        <format> literal {HEX|ASCii|DEC|BIN|LINE} default ASCII
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:FORMat?'))
    @format.setter
    def format(self, format:DecoderFormat):
        self.visa.write(f':DECoder{self._decoder}:FORMat {format}')
        return
    
  
    @property
    def position(self) -> int:
        '''
        DECODER{0|1}:POSITION[?] <position>
        Set or query the vertical position of the bus on the screen.

        <position> Integer 50 to 350
        default     Decoder 1: 350
                    Decoder 2: 300
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:POSition?'))
    @position.setter
    def position(self, position:int):
        if position < 50: position = 50
        if position > 350: position = 350
        self.visa.write(f':DECoder{self._decoder}:POSition {position}')
        return
    
    @property
    def threshold_chan1(self) -> float:
        '''
        :DECODER{0:1}:THRESHOLD:CHANNEL1[?] <threshold>
        Set or query the threshold level of the specified analog channel.

        <threshold> Real (-4 x VerticalScale - VerticalOffset) to
                         ( 4 x VerticalScale - VerticalOffset)
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel1?'))
    @threshold_chan1.setter
    def threshold_chan1(self, threshold:float):
        chan = 1
        threshold = self._verify_threshold(chan, threshold) 
        self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {threshold}')
        return
    
    @property
    def threshold_chan2(self) -> float:
        '''
        :DECODER{0:1}:THRESHOLD:CHANNEL2[?] <threshold>
        Set or query the threshold level of the specified analog channel.

        <threshold> Real (-4 x VerticalScale - VerticalOffset) to
                         ( 4 x VerticalScale - VerticalOffset)
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel2?'))
    @threshold_chan2.setter
    def threshold_chan2(self, threshold:float):
        chan = 2
        threshold = self._verify_threshold(chan, threshold)
        self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {threshold}')
        return
    
    @property
    def threshold_chan3(self) -> float:
        '''
        :DECODER{0:1}:THRESHOLD:CHANNEL3[?] <threshold>
        Set or query the threshold level of the specified analog channel.

        <threshold> Real (-4 x VerticalScale - VerticalOffset) to
                         ( 4 x VerticalScale - VerticalOffset)
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel3?'))
    @threshold_chan3.setter
    def threshold_chan1(self, threshold:float):
        chan = 3
        threshold = self._verify_threshold(chan, threshold)
        self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {threshold}')
        return
     
    @property
    def threshold_chan4(self) -> float:
        '''
        :DECODER{0:1}:THRESHOLD:CHANNEL4[?] <threshold>
        Set or query the threshold level of the specified analog channel.

        <thresh> Real (-4 x VerticalScale - VerticalOffset) to
                      (4 x VerticalScale - VerticalOffset)
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel4?'))
    @threshold_chan4.setter
    def threshold_chan4(self, threshold:float):
        chan = 4
        threshold = self._verify_threshold(chan, threshold) 
        self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {threshold}')
        return
    
    def _verify_threshold(self, chan, thresh):
        v_scale = self.visa.query(f":CHAN{chan}:SCALe?")
        v_offset = self.visa.query(f":CHAN{chan}:OFFSet?")
        if thresh < (-4*v_scale - v_offset): thresh = (-4*v_scale - v_offset)
        if thresh > ( 4*v_scale + v_offset): thresh = ( 4*v_scale + v_offset) 
        return thresh
    
     
    @property
    def threshold_auto(self) -> OnOff:
        '''
        :DECODER{0:1}:THRESHOLD:AUTO[?] <threshold>
        Turn on or off the auto threshold function of the analog channels, or query the status of
        the auto threshold function of the analog channels.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:THREshold:AUTO?'))
    @threshold_auto.setter
    def threshold_auto(self, auto_on_off:OnOff):
        self.visa.write(f':DECoder{self._decoder}:THREshold:AUTO {auto_on_off}')
        return
    
    @property
    def config_label(self) -> OnOff:
        '''
        :DECODER{0:1}:CONFIG:LABEL[?] <threshold>
        Turn on or off the label display function, or query the status of the label display function.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:CONFig:LABel?'))
    @config_label.setter
    def config_label(self, label:OnOff):
        self.visa.write(f':DECoder{self._decoder}:CONFig:LABel {label}')
        return
    
    @property
    def config_line(self) -> OnOff:
        '''
        Turn on or off the label display function, or query the status of the label display function.

        When this function is enabled, the bus will be displayed on the screen. You can send
        the :DECoder<n>:POSition command to adjust the vertical display position of the bus.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:CONFig:LINE?'))
    @config_line.setter
    def config_line(self, line:OnOff):
        self.visa.write(f':DECoder{self._decoder}:CONFig:LINE {line}')
        return
    
    @property
    def config_format(self) -> OnOff:
        '''
        Turn on or off the format display function, or query the status of the format display function.

        When this function is turned on, the current bus display format will be displayed at the
        right of the label display (when the bus display is turned on). You can send
        the :DECoder<n>:FORMat command to set the bus display format.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:CONFig:FORMAT?'))
    @config_format.setter
    def config_format(self, format:OnOff):
        self.visa.write(f':DECoder{self._decoder}:CONFig:FORMAT {format}')
        return
    
    
    @property
    def config_endian(self) -> OnOff:
        '''
        Turn on or off the endian display function in serial bus decoding, or query the status of
        the endian display function in serial bus decoding.

        When this function is enabled, the current bus endian will be displayed at the right of
        the format display (when the bus display is turned on).

        This command is invalid in parallel decoding.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:CONFig:ENDIan?'))
    @config_endian.setter
    def config_endian(self, endian:OnOff):
        self.visa.write(f':DECoder{self._decoder}:CONFig:ENDIan {endian}')
        return
    

    @property
    def config_width(self) -> OnOff:
        '''
        Turn on or off the width display function, or query the status of the width display function.

        When this function is enabled, the width of each frame of data will be displayed at the
        right of the endian display (when the bus display is turned on).   
        '''
        return (self.visa.query(f':DECoder{self._decoder}:CONFig:WIDth?'))
    @config_width.setter
    def config_width(self, width:OnOff):
        self.visa.write(f':DECoder{self._decoder}:CONFig:WIDth {width}')
        return
    

    @property
    def config_samplerate(self) -> float:
        '''
        :DECODER{0|1}:CONFIG:SRATE?
        Query the current digital sample rate.  

        The digital sample rate is related to the data source currently selected. By default, the
        data source is "Trace"; at this point, the digital sample rate is related to the horizontal
        time base. 
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:CONFig:SRATe?'))
    
# ==================================================================================
# ========                        UART                                     =========
# ==================================================================================

    def setup_uart(self, tx_chan:DecoderChannel, rx_chan:DecoderChannel, baud:int):
        self.uart_tx = tx_chan
        self.uart_rx = rx_chan
        self.uart_baud = baud

    @property
    def uart_tx(self) -> DecoderChannel:
        '''
        :DECODER{0|1}:UART:TX[?] <channel>
        Set or query the TX channel source of RS232 decoding. 

        When OFF is selected, no TX channel source will be set. The TX channel source and RX
        channel source (:DECoder<n>:UART:RX) cannot be both set to OFF.  
        '''
        return (self.visa.query(f':DECoder{self._decoder}:UART:TX?'))
    @uart_tx.setter
    def uart_tx(self, channel:DecoderChannel):
        self.visa.write(f':DECoder{self._decoder}:UART:TX {channel}')
        return
    
    @property
    def uart_rx(self) -> DecoderChannel:
        '''
        :DECODER{0|1}:UART:RX[?] <channel>
        Set or query the RX channel source of RS232 decoding. 

        When OFF is selected, no RX channel source will be set. The RX channel source and TX
        channel source (:DECoder<n>:UART:TX) cannot be both set to OFF.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:UART:RX?'))
    @uart_rx.setter
    def uart_rx(self, channel:DecoderChannel):
        self.visa.write(f':DECoder{self._decoder}:UART:RX {channel}')
        return
    
    
    @property
    def uart_polarity(self) -> Polarity:
        '''
        :DECODER{0|1}:UART:POLARITY[?] <polarity>
        Set or query the polarity of RS232 decoding.

        POSITIVE polarity high is 1 and low is 0.
        NEGATIVE polarity high is 0 and low is 1.  
        '''
        return (self.visa.query(f':DECoder{self._decoder}:UART:POLarity?'))
    @uart_polarity.setter
    def uart_polarity(self, polarity:Polarity):
        self.visa.write(f':DECoder{self._decoder}:UART:POLarity {polarity}')
        return

   
    @property
    def uart_endian(self) -> Endianess:
        '''
        Set or query the endian of RS232 decoding.  
        '''
        return (self.visa.query(f':DECoder{self._decoder}:UART:ENDIan?'))
    @uart_endian.setter
    def uart_endian(self, endianess:Endianess):
        self.visa.write(f':DECoder{self._decoder}:UART:ENDIan {endianess}')
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
        :DECODER{0|1}:UART:WIDTH[?] <frame_width>
        Set or query the width of each frame of data in RS232 decoding.

        frame_width is an integer between 5 and 8; default 8.
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:UART:WIDth?'))
    @uart_width.setter
    def uart_width(self, frame_width:int):
        if (frame_width < 5): frame_width = 5
        if (frame_width > 8): frame_width = 8
        self.visa.write(f':DECoder{self._decoder}:UART:WIDth {frame_width}')
        return
    
    
    @property
    def uart_stop_bit(self) -> UartStopBits:
        '''
        :DECODER{0|1}:UART:STOP[?] <stop_bit>
        Set or query the stop bit after each frame of data in RS232 decoding.

        stop_bit is 1, 1.5, or 2; Default 1.
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:UART:STOP?'))
    @uart_stop_bit.setter
    def uart_stop_bit(self, stop_bit:UartStopBits):
        self.visa.write(f':DECoder{self._decoder}:UART:STOP {stop_bit}')
        return
    

    @property
    def uart_parity(self) -> UartParity:
        '''
        Set or query the even-odd check mode of the data transmission in RS232 decoding.

        Parity is {NONE|EVEN|ODD}; Default NONE
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:UART:PARity?'))
    @uart_parity.setter
    def uart_parity(self, parity:UartParity):
        self.visa.write(f':DECoder{self._decoder}:UART:PARity {parity}')
        return
    

# ==================================================================================
# ========                        I2C                                      =========
# ==================================================================================

    def i2c_setup(self, clock:DecoderChannel, data:DecoderChannel):
        self.i2c_clock = clock
        self.i2c_data  = data

    @property
    def i2c_clock(self) -> DecoderChannel:
        '''
        :DECoder{0|1}:IIC:CLK[?] <channel>
        Set or query the signal source of the clock channel in I2C decoding.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:IIC:CLK?'))
    @i2c_clock.setter
    def i2c_clock(self, channel:DecoderChannel):
        self.visa.write(f':DECoder{self._decoder}:IIC:CLK {channel}')
        return


    @property
    def i2c_data(self) -> DecoderChannel:
        '''
        :DECoder{0|1}:IIC:DATA[?] <channel>
        Set or query the signal source of the data channel in I2C decoding.
        '''
        return (self.visa.query(f':DECoder{self._decoder}:IIC:DATA?'))
    @i2c_data.setter
    def i2c_data(self, channel:DecoderChannel):
        self.visa.write(f':DECoder{self._decoder}:IIC:DATA {channel}')
        return
    

    @property
    def i2c_address_mode(self) -> I2CAddressMode:
        '''
        :DECODER{0|1}:IIC:ADDRESS[?] <address_mode>
        Set or query the address mode of I2C decoding.

        <address_mode> {NORMal|RW}  Default: NORMAL

        NORMal: the address bits (:TRIGger:IIC:AWIDth) does not include the R/W bit.
        RW: the address bits (:TRIGger:IIC:AWIDth) includes the R/W bit.
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:IIC:ADDRess?'))
    @i2c_data.setter
    def i2c_data(self, address_mode:I2CAddressMode):
        self.visa.write(f':DECoder{self._decoder}:IIC:ADDRess {address_mode}')
        return

# ==================================================================================
# ========                        SPI                                      =========
# ==================================================================================

    def setup_spi(self, clock:DecoderChannel, miso:DecoderChannel, mosi:DecoderChannel, cs:DecoderChannel):
        self.spi_clock = clock
        self.spi_miso  = miso
        self.spi_mosi  = mosi
        self.spi_cs    = cs

    @property
    def spi_clock(self) -> DecoderChannel:
        '''
        :DECODER{0|1}:SPI:CLK[?] <channel>
        Set or query the signal source of the clock channel in SPI decoding.
        '''
        return str(self.visa.query(f':DECoder{self._decoder}:SPI:CLK?'))
    @i2c_clock.setter
    def i2c_clock(self, channel:DecoderChannel):
        self.visa.write(f':DECoder{self._decoder}:SPI:CLK {channel}')
        return

    @property
    def spi_miso(self) -> DecoderChannel:
        '''
        :DECODER{0|1}:SPI:MISO[?] <channel>
        Set or query the signal source of the clock channel in SPI decoding.
        '''
        return str(self.visa.query(f':DECoder{self._decoder}:SPI:MISO?'))
    @spi_miso.setter
    def spi_miso(self, channel:DecoderChannel):
        self.visa.write(f':DECoder{self._decoder}:SPI:MISO {channel}')
        return


    @property
    def spi_mosi(self) -> DecoderChannel:
        '''
        :DECODER{0|1}:SPI:MOSI[?] <channel>
        Set or query the signal source of the clock channel in SPI decoding.
        '''
        return str(self.visa.query(f':DECoder{self._decoder}:SPI:MOSI?'))
    @spi_mosi.setter
    def spi_mosi(self, channel:DecoderChannel):
        self.visa.write(f':DECoder{self._decoder}:SPI:MOSI {channel}')
        return

    @property
    def spi_cs(self) -> DecoderChannel:
        '''
        :DECODER{0|1}:SPI:CS[?] <channel>
        Set or query the signal source of the clock channel in SPI decoding.
        '''
        return str(self.visa.query(f':DECoder{self._decoder}:SPI:CS?'))
    @spi_cs.setter
    def spi_cs(self, channel:DecoderChannel):
        self.visa.write(f':DECoder{self._decoder}:SPI:CS {channel}')
        return
    
    @property
    def spi_cs_polarity(self) -> str:
        '''
        Set or query the CS polarity in SPI decoding.

        This command is only valid in the CS mode (:DECoder<n>:SPI:MODE).
        '''
        return str(self.visa.query(f':DECoder{self._decoder}:SPI:SELect?'))
    @spi_cs_polarity.setter
    def spi_cs_polarity(self, cs_polarity:Polarity):
        if cs_polarity == "NEG":
            pol = "NCS"
        else:
            pol = "CS"
        self.visa.write(f':DECoder{self._decoder}:SPI:SELect {pol}')
        return


    @property
    def spi_frame_sync_mode(self) -> SpiTimeout:
        '''
        :DECoder{0|1}:SPI:ENDIAN[?] <endianess>
        Set or query the frame synchronization mode of SPI decoding.

        CS: it contains a chip select line (CS). You can perform frame synchronization
        according to CS. At this point, you need to send the :DECoder<n>:SPI:CS
        and :DECoder<n>:SPI:SELect commands to set the CS channel source and polarity.
        
        TIMeout: you can perform frame synchronization according to the timeout time. At
        this point, you need to send the :DECoder<n>:SPI:TIMeout command to set the
        timeout time.

        <cs_timeout> Discrete {CS|TIMeout} TIMeout
        '''
        return str(self.visa.query(f':DECoder{self._decoder}:SPI:MODE?'))
    @spi_frame_sync_mode.setter
    def spi_frame_sync_mode(self, frame_sync_timeout:SpiTimeout):
        self.visa.write(f':DECoder{self._decoder}:SPI:MODE {frame_sync_timeout}')
        return
    
    @property
    def spi_timeout(self) -> float:
        '''
        :DECoder{0|1}:SPI:TIMEOUT[?] <timeout>
        Set or query the timeout time in the timeout mode of SPI decoding. The default unit is s.           

        The timeout time should be greater than the maximum pulse width of the clock and
        lower than the idle time between frames.

        This command is only valid in the timeout mode (:DECoder<n>:SPI:MODE).
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:SPI:TIMeout?'))
    @spi_timeout.setter
    def spi_timeout(self, timeout:float):
        #todo: return if spi_frame_sync_mode is CS??
        self.visa.write(f':DECoder{self._decoder}:SPI:TIMeout {timeout}')
        return
    

    @property
    def spi_polarity(self) -> Polarity:
        '''
        :DECoder{0|1}:SPI:POLARITY[?] <polarity>
        Set or query the timeout time in the timeout mode of SPI decoding. The default unit is s.           

        The timeout time should be greater than the maximum pulse width of the clock and
        lower than the idle time between frames.

        This command is only valid in the timeout mode (:DECoder<n>:SPI:MODE).
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:SPI:POLarity?'))
    @spi_polarity.setter
    def spi_polarity(self, polarity:Polarity):
        self.visa.write(f':DECoder{self._decoder}:SPI:POLarity {polarity}')
        return
    

    @property
    def spi_edge(self) -> SpiEdge:
        '''
        :DECoder{0|1}:SPI:EDGE[?] <edge>
        Set or query the clock type when the instrument samples the data line in SPI decoding.
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:SPI:EDGE?'))
    @spi_edge.setter
    def spi_edge(self, edge:SpiEdge):
        self.visa.write(f':DECoder{self._decoder}:SPI:EDGE {edge}')
        return
    
    @property
    def spi_endian(self) -> str:
        '''
        :DECoder{0|1}:SPI:ENDIAN[?] <endianess>
        Set or query the endian of the SPI decoding data.

        LSB or MSB, default MSB
        '''
        return float(self.visa.query(f':DECoder{self._decoder}:SPI:ENDian?'))
    @spi_endian.setter
    def spi_endian(self, endianess:Endianess):
        self.visa.write(f':DECoder{self._decoder}:SPI:ENDian {endianess}')
        return
    
    @property
    def spi_width(self) -> int:
        '''
        :DECoder{0|1}:SPI:WIDTh[?] <width>
        Set or query the number of bits of each frame of data in SPI decoding.
        '''
        return int(self.visa.query(f':DECoder{self._decoder}:SPI:WIDTh?'))
    @spi_width.setter
    def spi_width(self, width:int):
        if width < 8:  width = 8
        if width > 32: width = 32
        self.visa.write(f':DECoder{self._decoder}:SPI:WIDTh {width}')
        return
    


# ==================================================================================
# ========                        PARALLEL                                 =========
# ==================================================================================

#TODO

