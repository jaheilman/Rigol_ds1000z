from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import WaveSource, WaveMode, WaveFormat
import numpy as np

class Rigol_ds1000z_Wave():
    '''
    Handles the channels configuration (vertical axis).
    One instance of this class should be instanciated for each channel
    '''

    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)

    @property
    def source(self) -> WaveSource:
        '''
        Set or query the channel of which the waveform data will be read,

        <source>    {D0|D1|D2|D3|D4|D5|D6|D7|D8|
                    D9|D10|D11|D12|D13|D14|D15|
                    CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH}
        default: CHANnel1
        '''
        return self.visa.query(f':WAVeform:SOURce?')
    @source.setter
    def source(self, source:WaveSource):
        self.visa.write(f':WAVeform:SOURce {source}')
        return
    
    @property
    def mode(self) -> WaveMode:
        '''
        Set or query the reading mode used by :WAVeform:DATA?

        <mode> Discrete {NORMal|MAXimum|RAW} default: NORMal
        '''
        return self.visa.query(f':WAVeform:MODE?')
    @mode.setter
    def mode(self, mode:WaveMode):
        self.visa.write(f':WAVeform:MODE {mode}')
        return
    
    @property
    def format(self) -> WaveFormat:
        '''
        Set or query the return format of the waveform data

        <format> Discrete {WORD|BYTE|ASCii} default: BYTE
        '''
        return self.visa.query(f':WAVeform:FORMat?')
    @format.setter
    def format(self, format:WaveFormat):
        self.visa.write(f':WAVeform:FORMat {format}')
        return
    
    @property
    def data(self):
        '''
        Reading procedures of the screen waveform data:
        S1. :WAV:SOUR CHAN1 Set the channel source to CH1
        S2. :WAV:MODE NORM Set the waveform reading mode to NORMal
        S3. :WAV:FORM BYTE Set the return format of the waveform data to BYTE
        S4. :WAV:DATA? Read the screen waveform data

        Mode Max Number Datapoints That Can be read
        BYTE 250000
        WORD 125000
        ASCii 15625

        When the memory depth of the scope is greater than the number of points 
        that can be read, one must perform multiple block reads using START and STOP
        to define the blocks.
        '''
        return self.visa.write_read_raw(f':WAVeform:DATA?')

    @property
    def x_increment(self) -> float:
        '''
        Query the time difference between two neighboring points of the 
        specified channel source in the X direction

        The query returns the XINCrement as float
        '''
        return float(self.visa.query(f':WAVeform:XINCrement?'))

    @property
    def x_origin(self) -> float:
        '''
        Query the start time of the waveform data of the channel source 
        currently selected in the X direction.

        The query returns the Xorigin as float, related to the current wave mode:

        In NORMal mode, the query returns the start time of the waveform data displayed on
        the screen.

        In RAW mode, the query returns the start time of the waveform data in the internal
        memory.

        In MAX mode, the query returns the start time of the waveform data displayed on the
        screen when the instrument is in running status; the query returns the start time of
        the waveform data in the internal memory when the instrument is in stop status.
        
        '''
        return float(self.visa.query(f':WAVeform:XORigin?'))
    
    @property
    def x_reference(self) -> float:
        '''
        Query the reference time of the specified channel source in the X direction
        
        '''
        return float(self.visa.query(f':WAVeform:XREFerence?'))
    
    @property
    def y_increment(self) -> float:
        '''
        Query the waveform increment of the specified channel source in the Y direction. The unit
        is the same as the current amplitude unit.

        The return value is related to the current data reading mode:
        In NORMal mode, YINCrement = VerticalScale/25.
        In RAW mode, YINCrement is related to the Verticalscale of the internal waveform and the
        Verticalscale currently selected.
        In MAX mode, YINCrement = VerticalScale/25 when the instrument is in running status;
        YINCrement is related to the Verticalscale of the internal waveform and the Verticalscale
        currently selected when the instrument is in stop status
        
        '''
        return float(self.visa.query(f':WAVeform:YINCrement?'))

    @property
    def y_origin(self) -> int:
        '''
        Query the vertical offset relative to the vertical reference 
        position of the specified channel source in the Y direction.

        The return value is an integeter related to the current data reading mode:
        In NORMal mode, YORigin = VerticalOffset/YINCrement.
        In RAW mode, YORigin is related to the Verticalscale of the internal waveform and the
        Verticalscale currently selected.
        In MAX mode, YORigin = VerticalOffset/YINCrement when the instrument is in running
        status; YORigin is related to the Verticalscale of the internal waveform and the
        Verticalscale currently selected when the instrument is in stop status.
        
        '''
        return int(self.visa.query(f':WAVeform:YORigin?'))
    
    @property
    def y_reference(self) -> int:
        '''
        Query the vertical reference position of the specified channel source in the Y direction.

        Always returns 127 (0 = bottom of screen, 255 = top of screen)
        '''
        return float(self.visa.query(f':WAVeform:YREFerence?'))
    
    @property
    def start(self) -> int:
        '''
        Set or query the start point of waveform data reading

        <start> Integer default 0
        NORMal: 1 to 1200
        MAX: 1 to the number of effective points currently on the screen
        RAW: 1 to the current maximum memory depth
1
        '''
        return int(self.visa.query(f':WAVeform:STARt?'))
    @start.setter
    def start(self, start:int):
        self.visa.write(f':WAVeform:STARt {start}')
        return
    
    @property
    def stop(self) -> int:
        '''
        Set or query the stop point of waveform data reading

        <stop> Integer  default: 1200
        NORMal: 1 to 1200
        MAX: 1 to the number of effective points currently on the screen
        RAW: 1 to the current maximum memory depth
1
        '''
        return int(self.visa.query(f':WAVeform:STOP?'))
    @stop.setter
    def stop(self, stop:int):
        self.visa.write(f':WAVeform:STOP {stop}')
        return
    
    @property
    def preamble(self) -> dict:
        '''
        Query returns 10 waveform parameters separated by ","

        <format>,<type>,<points>,<count>,<xincrement>,<xorigin>,
        <xreference>,<yincrement>,<yorigin>,<yreference>
        '''
        pre = self.visa.query('WAVeform:PREamble?').split(',')
        pre_dict = {
            'format': int(pre[0]),
            'type': int(pre[1]),
            'points': int(pre[2]),
            'count': int(pre[3]),
            'xincrement': float(pre[4]),
            'xorigin': float(pre[5]),
            'xreference': float(pre[6]),
            'yincrement': float(pre[7]),
            'yorigin': float(pre[8]),
            'yreference': float(pre[9]),
        }
        return pre_dict
    
    # Helper scripts

    def get_wavedata(self, 
        source=WaveSource.CHAN1, 
        mode=WaveMode.NORMAL,
        ) -> list: 
        '''
        Download the captured voltage points from the oscilloscope.

        Args:
            source (WaveSource): channel, digital, or Math source
            mode (WaveMode): Normal, Max, or Raw
            format is fixed as BYTE 

        Returns: 2D list
            list[0] time values
            list[1] voltage values
        '''
        # assert mode in ('norm', 'raw')

        # Setup scope
        self.visa.write(f':stop') # can't access parent
        self.source = source
        self.mode = mode
        format = WaveFormat.BYTE
        self.format = format

        preamble = self.preamble

        readout_pts_byte_format = 250000
        readout_pts_word_format = 125000
        readout_pts_ascii_format = 15625

        readout_pts = readout_pts_byte_format
        num_blocks = preamble['points'] // readout_pts # floor division
        last_block_pts = preamble['points'] % readout_pts # modulo

        datas = []
        for i in range(num_blocks+1):
            if i < num_blocks:
                self.start = (1+i*readout_pts)
                self.stop = (readout_pts*(i+1))
            else:
                if last_block_pts:
                    self.start = (1+num_blocks*readout_pts)
                    self.stop = (num_blocks*readout_pts+last_block_pts)
                else:
                    break
            mydata = self.visa.write_read_raw(':wav:data?')
            data = mydata[11:]
            data = np.frombuffer(data, 'B')
            datas.append(data)

        datas = np.concatenate(datas)
        v = (datas - preamble['yorigin'] - preamble['yreference']) * preamble['yincrement']
        t = np.arange(0, preamble['points']*preamble['xincrement'], preamble['xincrement'])
        return_list = [t.tolist(), v.tolist()]
        return return_list