from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import MemoryDepth, AcquisitionMode
import math

class Rigol_ds1000z_Acquire:
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)

    @property
    def averages(self) -> int:
        '''
        Set or query the number of averages under the average acquisition mode

        averages is 2^n where is an integer from 1 to 10
        if count is not a power of 2, it will be rounded down to the nearest
        power of 2
        '''
        return int(self.visa.query(':acq:averages?'))
    @averages.setter
    def averages(self, averages:int):
        averages = 2**(math.floor(math.log2(averages)))
        self.visa.write(f':acq:averages {averages}')
        return

    @property
    def type(self) -> str:
        '''
        Set or query the acquisition mode of the oscilloscope.

        mode = {NORMal|AVERages|PEAK|HRESolution}
        '''
        return self.visa.query(':acq:type?')
    @type.setter
    def type(self, mode:AcquisitionMode):
        self.visa.write(f':acq:type {mode}')


    @property
    def sample_rate(self) -> int:
        '''
        Query the current sample rate. The default unit is Sa/s.
        
        Sample rate is the sample frequency of the oscilloscope, namely the waveform points
        sampled per second.
        The following equation describes the relationship among memory depth, sample
        rate, and waveform length:
            Memory Depth = Sample Rate x Waveform Length
        Wherein, the Memory Depth can be set using the :ACQuire:MDEPth command, and
        the Waveform Length is the product of the horizontal timebase (set by
        the :TIMebase[:MAIN]:SCALe command) times the number of the horizontal scales
        (12 for DS1000Z).
        
        Return Format: The query returns the sample rate (integer).
        '''
        return int(float(self.visa.query(':acq:srat?')))

    @property
    def memory_depth(self):
        '''
        Set or query the memory depth of the oscilloscope (namely the number of waveform
        points that can be stored in a single trigger sample). The default unit is pts (points).

        For the analog channel:
        ― When a single channel is enabled, the range of <mdep> is 
        {AUTO|12000|120000|1200000|12000000|24000000}.
        ― When dual channels are enabled, the range of <mdep> is 
         {AUTO|6000|60000|600000|6000000|12000000}.
        ― When three/four channels are enabled, the range of <mdep> is 
          {AUTO|3000|30000|300000|3000000|6000000}.

        For the digital channel:
        ― When 8 channels are enabled, the range of <mdep> is 
          {AUTO|12000|120000|1200000|12000000|24000000}.
        ― When 16 channels are enabled, the range of <mdep> is
          {AUTO|6000|60000|600000|6000000|12000000}.
        
        The following equation describes the relationship among memory depth, sample
        rate, and waveform length:
           Memory Depth = Sample Rate x Waveform Length
        Wherein, the Waveform Length is the product of the horizontal timebase (set by
        the :TIMebase[:MAIN]:SCALe command) times the number of grids in the horizontal
        direction on the screen (12 for DS1000Z).
        When AUTO is selected, the oscilloscope will select the memory depth automatically
        according to the current sample rate.

        The query returns the actual number of points (integer) or AUTO.
        '''
        md = self.visa.query(':acq:mdep?')
        return int(md) if not md.startswith('AUTO') else md
    @memory_depth.setter
    def memory_depth(self, memory_depth:MemoryDepth):
        num_enabled_chans = self._channels_enabled()
        # Resort to AUTO if improper number of pts specified
        if num_enabled_chans == 1:
            if pts not in ('AUTO', '12000', '120000', '1200000', '12000000', '24000000'):
                pts = 'AUTO'
        elif num_enabled_chans == 2:
            if pts not in ('AUTO', '6000', '60000', '600000', '6000000', '12000000'):
                pts = 'AUTO'
        elif num_enabled_chans in (3, 4):
            if pts not in ('AUTO', '3000', '30000', '300000', '3000000', '6000000'):
                pts = 'AUTO'
        self.run()
        self.visa.write(f':acq:mdep {pts}')


    def _channels_enabled(self) -> int:
        channels_enabled = 0
        for chan in ['CHAN1', 'CHAN2', 'CHAN3', 'CHAN4']:
            channels_enable += self.visa.query(f':{chan}:DISPplay?')
        return channels_enabled
