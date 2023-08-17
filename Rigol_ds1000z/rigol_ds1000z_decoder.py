from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import class_has_value, OnOff, Polarity, Endianess,Edge, \
    DecoderMode, DecoderFormat, DecoderChannel, \
    UartParity, UartStopBits, I2CAddressMode, SpiEdge, SpiTimeout

    
class Rigol_ds1000z_Decoder:
    def __init__(self, visa_resource, n_decoder):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)
        self._decoder = n_decoder
        self.threshold = self.Threshold(visa_resource)
        self.uart = self.UART(visa_resource)
        self.i2c = self.I2C(visa_resource)
        self.spi = self.SPI(visa_resource)
        self.parallel = self.Parallel(visa_resource)



    @property
    def mode(self) -> DecoderMode:
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
    def format(self) -> DecoderFormat:
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
    
    class Threshold:
        def __init__(self, visa_resource):
            self.visa_resource = visa_resource
            self.visa = Rigol_visa(visa_resource)

        @property
        def chan1(self) -> float:
            '''
            :DECODER{0:1}:THRESHOLD:CHANNEL1[?] <threshold>
            Set or query the threshold level of the specified analog channel.

            <threshold> Real (-4 x VerticalScale - VerticalOffset) to
                            ( 4 x VerticalScale - VerticalOffset)
            '''
            return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel1?'))
        @chan1.setter
        def chan1(self, threshold:float):
            chan = 1
            threshold = self._verify_threshold(chan, threshold) 
            self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {threshold}')
            return
        
        @property
        def chan2(self) -> float:
            '''
            :DECODER{0:1}:THRESHOLD:CHANNEL2[?] <threshold>
            Set or query the threshold level of the specified analog channel.

            <threshold> Real (-4 x VerticalScale - VerticalOffset) to
                            ( 4 x VerticalScale - VerticalOffset)
            '''
            return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel2?'))
        @chan2.setter
        def chan2(self, threshold:float):
            chan = 2
            threshold = self._verify_threshold(chan, threshold)
            self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {threshold}')
            return
        
        @property
        def chan3(self) -> float:
            '''
            :DECODER{0:1}:THRESHOLD:CHANNEL3[?] <threshold>
            Set or query the threshold level of the specified analog channel.

            <threshold> Real (-4 x VerticalScale - VerticalOffset) to
                            ( 4 x VerticalScale - VerticalOffset)
            '''
            return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel3?'))
        @chan3.setter
        def chan3(self, threshold:float):
            chan = 3
            threshold = self._verify_threshold(chan, threshold)
            self.visa.write(f':DECoder{self._decoder}:THREshold:CHANnel{chan} {threshold}')
            return
        
        @property
        def chan4(self) -> float:
            '''
            :DECODER{0:1}:THRESHOLD:CHANNEL4[?] <threshold>
            Set or query the threshold level of the specified analog channel.

            <thresh> Real (-4 x VerticalScale - VerticalOffset) to
                        (4 x VerticalScale - VerticalOffset)
            '''
            return float(self.visa.query(f':DECoder{self._decoder}:THREshold:CHANnel4?'))
        @chan4.setter
        def chan4(self, threshold:float):
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
        def auto(self) -> OnOff:
            '''
            :DECODER{0:1}:THRESHOLD:AUTO[?] <threshold>
            Turn on or off the auto threshold function of the analog channels, or query the status of
            the auto threshold function of the analog channels.
            '''
            return (self.visa.query(f':DECoder{self._decoder}:THREshold:AUTO?'))
        @auto.setter
        def auto(self, auto_on_off:OnOff):
            self.visa.write(f':DECoder{self._decoder}:THREshold:AUTO {auto_on_off}')
            return
    
    class Configure:
        def __init__(self, visa_resource):
            self.visa_resource = visa_resource
            self.visa = Rigol_visa(visa_resource)
            
        @property
        def label(self) -> OnOff:
            '''
            :DECODER{0:1}:CONFIG:LABEL[?] <threshold>
            Turn on or off the label display function, or query the status of the label display function.
            '''
            return (self.visa.query(f':DECoder{self._decoder}:CONFig:LABel?'))
        @label.setter
        def label(self, label:OnOff):
            self.visa.write(f':DECoder{self._decoder}:CONFig:LABel {label}')
            return
        
        @property
        def line(self) -> OnOff:
            '''
            Turn on or off the label display function, or query the status of the label display function.

            When this function is enabled, the bus will be displayed on the screen. You can send
            the :DECoder<n>:POSition command to adjust the vertical display position of the bus.
            '''
            return (self.visa.query(f':DECoder{self._decoder}:CONFig:LINE?'))
        @line.setter
        def line(self, line:OnOff):
            self.visa.write(f':DECoder{self._decoder}:CONFig:LINE {line}')
            return
        
        @property
        def format(self) -> OnOff:
            '''
            Turn on or off the format display function, or query the status of the format display function.

            When this function is turned on, the current bus display format will be displayed at the
            right of the label display (when the bus display is turned on). You can send
            the :DECoder<n>:FORMat command to set the bus display format.
            '''
            return (self.visa.query(f':DECoder{self._decoder}:CONFig:FORMAT?'))
        @format.setter
        def format(self, format:OnOff):
            self.visa.write(f':DECoder{self._decoder}:CONFig:FORMAT {format}')
            return
        
        
        @property
        def endian(self) -> OnOff:
            '''
            Turn on or off the endian display function in serial bus decoding, or query the status of
            the endian display function in serial bus decoding.

            When this function is enabled, the current bus endian will be displayed at the right of
            the format display (when the bus display is turned on).

            This command is invalid in parallel decoding.
            '''
            return (self.visa.query(f':DECoder{self._decoder}:CONFig:ENDIan?'))
        @endian.setter
        def endian(self, endian:OnOff):
            self.visa.write(f':DECoder{self._decoder}:CONFig:ENDIan {endian}')
            return
        

        @property
        def width(self) -> OnOff:
            '''
            Turn on or off the width display function, or query the status of the width display function.

            When this function is enabled, the width of each frame of data will be displayed at the
            right of the endian display (when the bus display is turned on).   
            '''
            return (self.visa.query(f':DECoder{self._decoder}:CONFig:WIDth?'))
        @width.setter
        def width(self, width:OnOff):
            self.visa.write(f':DECoder{self._decoder}:CONFig:WIDth {width}')
            return
        

        @property
        def samplerate(self) -> float:
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

    class UART:
        def __init__(self, visa_resource):
            self.visa_resource = visa_resource
            self.visa = Rigol_visa(visa_resource)
            
        def setup_uart(self, tx_chan:DecoderChannel, rx_chan:DecoderChannel, baud:int):
            '''
            Helper function to setup UART
            '''
            self.uart_tx = tx_chan
            self.uart_rx = rx_chan
            self.uart_baud = baud

        @property
        def tx(self) -> DecoderChannel:
            '''
            :DECODER{0|1}:UART:TX[?] <channel>
            Set or query the TX channel source of RS232 decoding. 

            When OFF is selected, no TX channel source will be set. The TX channel source and RX
            channel source (:DECoder<n>:UART:RX) cannot be both set to OFF.  
            '''
            return (self.visa.query(f':DECoder{self._decoder}:UART:TX?'))
        @tx.setter
        def tx(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:UART:TX {channel}')
            return
        
        @property
        def rx(self) -> DecoderChannel:
            '''
            :DECODER{0|1}:UART:RX[?] <channel>
            Set or query the RX channel source of RS232 decoding. 

            When OFF is selected, no RX channel source will be set. The RX channel source and TX
            channel source (:DECoder<n>:UART:TX) cannot be both set to OFF.
            '''
            return (self.visa.query(f':DECoder{self._decoder}:UART:RX?'))
        @rx.setter
        def rx(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:UART:RX {channel}')
            return
        
        
        @property
        def polarity(self) -> Polarity:
            '''
            :DECODER{0|1}:UART:POLARITY[?] <polarity>
            Set or query the polarity of RS232 decoding.

            POSITIVE polarity high is 1 and low is 0.
            NEGATIVE polarity high is 0 and low is 1.  
            '''
            return (self.visa.query(f':DECoder{self._decoder}:UART:POLarity?'))
        @polarity.setter
        def polarity(self, polarity:Polarity):
            self.visa.write(f':DECoder{self._decoder}:UART:POLarity {polarity}')
            return

    
        @property
        def endian(self) -> Endianess:
            '''
            Set or query the endian of RS232 decoding.  
            '''
            return (self.visa.query(f':DECoder{self._decoder}:UART:ENDIan?'))
        @endian.setter
        def endian(self, endianess:Endianess):
            self.visa.write(f':DECoder{self._decoder}:UART:ENDIan {endianess}')
            return
        

        @property
        def baud_rate(self) -> int:
            '''
            Set or query the buad rate of RS232 decoding. The default unit is bps (baud per second).

            The query returns the current baud rate in integer.  

            Baud rate must be <int> between 110 and 20M.  Default 9600
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:UART:BAUD?'))
        @baud_rate.setter
        def baud_rate(self, baud_rate:int):
            if (baud_rate < 110): baud_rate = 110
            if (baud_rate > 20000000): baud_rate = 20000000
            self.visa.write(f':DECoder{self._decoder}:UART:BAUD {baud_rate}')
            return
        

        @property
        def frame_width(self) -> int:
            '''
            :DECODER{0|1}:UART:WIDTH[?] <frame_width>
            Set or query the width of each frame of data in RS232 decoding.

            frame_width is an integer between 5 and 8; default 8.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:UART:WIDth?'))
        @frame_width.setter
        def frame_width(self, frame_width:int):
            if (frame_width < 5): frame_width = 5
            if (frame_width > 8): frame_width = 8
            self.visa.write(f':DECoder{self._decoder}:UART:WIDth {frame_width}')
            return
        
        
        @property
        def stop_bit(self) -> UartStopBits:
            '''
            :DECODER{0|1}:UART:STOP[?] <stop_bit>
            Set or query the stop bit after each frame of data in RS232 decoding.

            stop_bit is 1, 1.5, or 2; Default 1.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:UART:STOP?'))
        @stop_bit.setter
        def stop_bit(self, stop_bit:UartStopBits):
            self.visa.write(f':DECoder{self._decoder}:UART:STOP {stop_bit}')
            return
        

        @property
        def parity(self) -> UartParity:
            '''
            Set or query the even-odd check mode of the data transmission in RS232 decoding.

            Parity is {NONE|EVEN|ODD}; Default NONE
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:UART:PARity?'))
        @parity.setter
        def parity(self, parity:UartParity):
            self.visa.write(f':DECoder{self._decoder}:UART:PARity {parity}')
            return
    

# ==================================================================================
# ========                        I2C                                      =========
# ==================================================================================
    class I2C:
        def __init__(self, visa_resource):
            self.visa_resource = visa_resource
            self.visa = Rigol_visa(visa_resource)
            
        def setup_i2c(self, clock:DecoderChannel, data:DecoderChannel):
            self.i2c_clock = clock
            self.i2c_data  = data

        @property
        def clock(self) -> DecoderChannel:
            '''
            :DECoder{0|1}:IIC:CLK[?] <channel>
            Set or query the signal source of the clock channel in I2C decoding.
            '''
            return (self.visa.query(f':DECoder{self._decoder}:IIC:CLK?'))
        @clock.setter
        def clock(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:IIC:CLK {channel}')
            return


        @property
        def data(self) -> DecoderChannel:
            '''
            :DECoder{0|1}:IIC:DATA[?] <channel>
            Set or query the signal source of the data channel in I2C decoding.
            '''
            return (self.visa.query(f':DECoder{self._decoder}:IIC:DATA?'))
        @data.setter
        def data(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:IIC:DATA {channel}')
            return
        

        @property
        def address_mode(self) -> I2CAddressMode:
            '''
            :DECODER{0|1}:IIC:ADDRESS[?] <address_mode>
            Set or query the address mode of I2C decoding.

            <address_mode> {NORMal|RW}  Default: NORMAL

            NORMal: the address bits (:TRIGger:IIC:AWIDth) does not include the R/W bit.
            RW: the address bits (:TRIGger:IIC:AWIDth) includes the R/W bit.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:IIC:ADDRess?'))
        @address_mode.setter
        def address_mode(self, address_mode:I2CAddressMode):
            self.visa.write(f':DECoder{self._decoder}:IIC:ADDRess {address_mode}')
            return

# ==================================================================================
# ========                        SPI                                      =========
# ==================================================================================
    class SPI:
        def __init__(self, visa_resource):
            self.visa_resource = visa_resource
            self.visa = Rigol_visa(visa_resource)
            
        def setup_spi(self, clock:DecoderChannel, miso:DecoderChannel, mosi:DecoderChannel, cs:DecoderChannel):
            self.spi_clock = clock
            self.spi_miso  = miso
            self.spi_mosi  = mosi
            self.spi_cs    = cs

        @property
        def clock(self) -> DecoderChannel:
            '''
            :DECODER{0|1}:SPI:CLK[?] <channel>
            Set or query the signal source of the clock channel in SPI decoding.
            '''
            return str(self.visa.query(f':DECoder{self._decoder}:SPI:CLK?'))
        @clock.setter
        def clock(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:SPI:CLK {channel}')
            return

        @property
        def miso(self) -> DecoderChannel:
            '''
            :DECODER{0|1}:SPI:MISO[?] <channel>
            Set or query the signal source of the clock channel in SPI decoding.
            '''
            return str(self.visa.query(f':DECoder{self._decoder}:SPI:MISO?'))
        @miso.setter
        def miso(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:SPI:MISO {channel}')
            return


        @property
        def mosi(self) -> DecoderChannel:
            '''
            :DECODER{0|1}:SPI:MOSI[?] <channel>
            Set or query the signal source of the clock channel in SPI decoding.
            '''
            return str(self.visa.query(f':DECoder{self._decoder}:SPI:MOSI?'))
        @mosi.setter
        def mosi(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:SPI:MOSI {channel}')
            return

        @property
        def cs(self) -> DecoderChannel:
            '''
            :DECODER{0|1}:SPI:CS[?] <channel>
            Set or query the signal source of the clock channel in SPI decoding.
            '''
            return str(self.visa.query(f':DECoder{self._decoder}:SPI:CS?'))
        @cs.setter
        def cs(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:SPI:CS {channel}')
            return
        
        @property
        def cs_polarity(self) -> str:
            '''
            Set or query the CS polarity in SPI decoding.

            This command is only valid in the CS mode (:DECoder<n>:SPI:MODE).

            Returns NCS if negative, CS if positive
            '''
            return str(self.visa.query(f':DECoder{self._decoder}:SPI:SELect?'))
        @cs_polarity.setter
        def cs_polarity(self, cs_polarity:Polarity):
            if cs_polarity == "NEG":
                pol = "NCS"
            else:
                pol = "CS"
            self.visa.write(f':DECoder{self._decoder}:SPI:SELect {pol}')
            return


        @property
        def frame_sync_mode(self) -> SpiTimeout:
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
        @frame_sync_mode.setter
        def frame_sync_mode(self, frame_sync_timeout:SpiTimeout):
            self.visa.write(f':DECoder{self._decoder}:SPI:MODE {frame_sync_timeout}')
            return
        
        @property
        def timeout(self) -> float:
            '''
            :DECoder{0|1}:SPI:TIMEOUT[?] <timeout>
            Set or query the timeout time in the timeout mode of SPI decoding. The default unit is s.           

            The timeout time should be greater than the maximum pulse width of the clock and
            lower than the idle time between frames.

            This command is only valid in the timeout mode (:DECoder<n>:SPI:MODE).
            '''
            return float(self.visa.query(f':DECoder{self._decoder}:SPI:TIMeout?'))
        @timeout.setter
        def timeout(self, timeout:float):
            #todo: return if spi_frame_sync_mode is CS??
            self.visa.write(f':DECoder{self._decoder}:SPI:TIMeout {timeout}')
            return
        

        @property
        def polarity(self) -> Polarity:
            '''
            :DECoder{0|1}:SPI:POLARITY[?] <polarity>
            Set or query the timeout time in the timeout mode of SPI decoding. The default unit is s.           

            The timeout time should be greater than the maximum pulse width of the clock and
            lower than the idle time between frames.

            This command is only valid in the timeout mode (:DECoder<n>:SPI:MODE).
            '''
            return float(self.visa.query(f':DECoder{self._decoder}:SPI:POLarity?'))
        @polarity.setter
        def polarity(self, polarity:Polarity):
            self.visa.write(f':DECoder{self._decoder}:SPI:POLarity {polarity}')
            return
        

        @property
        def edge(self) -> SpiEdge:
            '''
            :DECoder{0|1}:SPI:EDGE[?] <edge>
            Set or query the clock type (edge) when the instrument samples the data line in SPI decoding.
            '''
            return float(self.visa.query(f':DECoder{self._decoder}:SPI:EDGE?'))
        @edge.setter
        def edge(self, edge:SpiEdge):
            self.visa.write(f':DECoder{self._decoder}:SPI:EDGE {edge}')
            return
        
        @property
        def endian(self) -> Endianess:
            '''
            :DECoder{0|1}:SPI:ENDIAN[?] <endianess>
            Set or query the endian of the SPI decoding data.

            LSB or MSB, default MSB
            '''
            return float(self.visa.query(f':DECoder{self._decoder}:SPI:ENDian?'))
        @endian.setter
        def endian(self, endianess:Endianess):
            self.visa.write(f':DECoder{self._decoder}:SPI:ENDian {endianess}')
            return
        
        @property
        def frame_width(self) -> int:
            '''
            :DECoder{0|1}:SPI:WIDTh[?] <width>
            Set or query the number of bits of each frame of data in SPI decoding.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:SPI:WIDTh?'))
        @frame_width.setter
        def frame_width(self, width:int):
            if width < 8:  width = 8
            if width > 32: width = 32
            self.visa.write(f':DECoder{self._decoder}:SPI:WIDTh {width}')
            return
    


# ==================================================================================
# ========                        PARALLEL                                 =========
# ==================================================================================

    class Parallel:
        def __init__(self, visa_resource):
            self.visa_resource = visa_resource
            self.visa = Rigol_visa(visa_resource)
            
        @property
        def clock(self) -> DecoderChannel:
            '''
            :DECoder<n>:PARallel:CLK
            Set or query the CLK channel source of parallel decoding.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:CLK?'))
        @clock.setter
        def clock(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:PARallel:CLK {channel}')
            return
        

        @property
        def edge(self) -> Edge:
            '''
            :DECoder<n>:PARallel:EDGE
            Set or query the edge type of the clock channel when the instrument samples the data
            channel in parallel decoding.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:EDGE?'))
        @edge.setter
        def edge(self, edge:Edge):
            self.visa.write(f':DECoder{self._decoder}:PARallel:EDGE {edge}')
            return
        
        @property
        def width(self) -> int:
            '''
            :DECoder<n>:PARallel:WIDTh
            Set or query the data width (namely the number of bits of each frame of data) of the
            parallel bus.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:WIDTH?'))
        @width.setter
        def width(self, bit_width:int):
            self.visa.write(f':DECoder{self._decoder}:PARallel:WIDTH {bit_width}')
            return
        
        @property
        def bitx(self) -> int:
            '''
            :DECoder<n>:PARallel:BITX
            Set or query the data bit that requires a channel source on the parallel bus.

            Set the data width using the :DECoder<n>:PARallel:WIDTh command.
            After selecting the desired bit, send the :DECoder<n>:PARallel:SOURce command to
            set the channel source of this bit.

            Example:
            :DECoder1:PARallel:BITX 2 /*Set the current bit to 2*/
            :DECoder1:PARallel:BITX? /*The query returns 2*/


            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:BITX?'))
        @bitx.setter
        def bitx(self, bit_width:int):
            self.visa.write(f':DECoder{self._decoder}:PARallel:BITX {bit_width}')
            return
        
        @property
        def bitx(self) -> DecoderChannel:
            '''
            :DECoder<n>:PARallel:SOURce
            Set ro query the channel source of the data bit currently selected.

            Before sending this command, use the :DECoder<n>:PARallel:BITX command to select
            the desired data bit.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:SOURce?'))
        @bitx.setter
        def bitx(self, channel:DecoderChannel):
            self.visa.write(f':DECoder{self._decoder}:PARallel:SOURce {channel}')
            return

        @property
        def polarity(self) -> Polarity:
            '''
            :DECoder<n>:PARallel:POLarity
            Set ro query the data polarity of parallel decoding.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:POLarity?'))
        @polarity.setter
        def polarity(self, polarity:Polarity):
            self.visa.write(f':DECoder{self._decoder}:PARallel:POLarity {polarity}')
            return

        @property
        def noise_rejection(self) -> OnOff:
            '''
            :DECoder<n>:PARallel:NREJect
            Turn on or off the noise rejection function of parallel decoding, or query the status of the
            noise rejection function of parallel decoding.

            Noise rejection can remove the data without enough duration on the bus to
            eliminate the glitches of the actual circuit.

            When the noise rejection is turned on, sending the :DECoder<n>:PARallel:NRTime
            command can set the desired rejection time.
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:NREJect?'))
        @noise_rejection.setter
        def noise_rejection(self, noise_reject:OnOff):
            self.visa.write(f':DECoder{self._decoder}:PARallel:NREJect {noise_reject}')
            return

    
        @property
        def noise_rejection_time(self) -> float:
            '''
            :DECoder<n>:PARallel:NRTime
            Set or query the noise rejection time of parallel decoding. The default unit is s.
            
            Range is 0.000s to 0.100s  

            Before sending this command, send the :DECoder<n>:PARallel:NREJect command to
            turn on the noise rejection function.            
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:NRTime?'))
        @noise_rejection_time.setter
        def noise_rejection_time(self, time_s:float):
            if time_s < 0: time_s = 0
            if time_s > 0.1: time_s = 0.1
            self.visa.write(f':DECoder{self._decoder}:PARallel:NRTime {time_s}')
            return  

        @property
        def clock_compenstation_time(self) -> float:
            '''
            :DECoder<n>:PARallel:CCOMpensation
            Set or query the clock compensation time of parallel decoding. The default unit is s.

            Range is -0.100s to 0.100s

            Setting the compensation time can make fine adjustment of the pahse deviation
            between the clock line and data line.

            This command is invalid when the CLK channel source is set to OFF
            (:DECoder<n>:PARallel:CLK).          
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:CCOM?'))
        @clock_compenstation_time.setter
        def clock_compenstation_time(self, time_s:float):
            if time_s < -0.1: time_s = -0.1
            if time_s >  0.1: time_s =  0.1
            self.visa.write(f':DECoder{self._decoder}:PARallel:CCOM {time_s}')
            return  

        @property
        def plot_curve(self) -> OnOff:
            '''
            :DECoder<n>:PARallel:PLOT
            Turn on or off the curve function of parallel decoding, or query the status of the curve
            function of parallel decoding.

            When this function is turned on, the variation trend of the bus data is displayed in vector
            diagram form.       
            '''
            return int(self.visa.query(f':DECoder{self._decoder}:PARallel:PLOT?'))
        @plot_curve.setter
        def plot_curve(self, plot:OnOff):
            self.visa.write(f':DECoder{self._decoder}:PARallel:PLOT {plot}')
            return  