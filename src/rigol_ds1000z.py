from rigol_visa import Rigol_visa
from rigol_ds1000z_acquire import Rigol_ds1000z_Acquire
from rigol_ds1000z_channel import Rigol_ds1000z_Channel

class Rigol_ds1000z:
    '''
    Rigol DS1000z series oscilloscope driver.

    Attributes:

    '''
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)
        self.num_channels = 4
        self.acquire = Rigol_ds1000z_Acquire(visa_resource)
        self.channel = [Rigol_ds1000z_Channel(c, self) for c in range(1, self.num_channels+1)]


    # self.trigger = _Rigol1000zTrigger(self)
    # self.timebase = _Rigol1000zTimebase(self)
        

    # def __getitem__(self, i):
    #     assert 1 <= i <= 4, 'Not a valid channel.'
    #     return self._channels[i-1]

    # def __len__(self):
    #     return len(self._channels)

    def autoscale(self):
        self.visa.write(':autoscale') 

    def clear(self):
        self.visa.write(':clear')

    def run(self):
        self.visa.write(':run')

    def stop(self):
        self.visa.write(':stop')

    def single(self):
        self.visa.write(':single')

    def force(self):
        self.visa.write(':tforce')


    # IEEE 488.2
    def cls(self):
        ''' 
        (IEEE 488.2)
        Clear all the event registers and clear the error queue.
        '''
        self.visa.write('*CLS')

    @property
    def ese(self) -> int:
        '''
        (IEEE 488.2)
        Set or query the enable register for the standard event status register set
        the range of <value> are the decimal numbers corresponding to 
        the binary numbers X0XXXX0X (X is 1 or 0).
        '''
        return self.visa.ask('*ESE?')
    @ese.setter
    def ese(self, val:int):
        self.visa.write(f'*ESE {val}')
    
    def esr(self) -> int:
        '''
        (IEEE 488.2)
        Query and clear the event register for the standard event status register.
        '''
        return self.visa.ask('*ESR?')

    def idn(self) -> str:
        '''
        (IEEE 488.2)
        Query the ID string of the instrument.
        '''
        return self.visa.ask('*IDN?')

    @property
    def opc(self) -> int:
        '''
        (IEEE 488.2)
        The *OPC command is used to set the Operation Complete bit (bit 0) in the standard
        event status register to 1 after the current operation is finished. The *OPC? command is
        used to query whether the current operation is finished.
        '''
        return self.visa.ask('*OPC?')
    @opc.setter
    def ese(self):
        self.visa.write('*OPC')

    def rst(self):
        '''
        (IEEE 488.2)
        Restore the instrument to the default state.
        '''
        self.visa.write('*RST')

    @property
    def sre(self) -> int:
        '''
        (IEEE 488.2)
        Set or query the enable register for the status byte register set.
        '''
        return self.visa.ask('*SRE?')
    @opc.setter
    def sre(self, val:int):
        self.visa.write(f'*SRE {val}')

    def stb(self) -> int:
        '''
        (IEEE 488.2)
        Query the event register for the status byte register. The value of the status byte register
        is set to 0 after this command is executed.
        
        The bit 0 and bit 1 of the status byte register are not used and are always treated as 0.
        The query returns the decimal numbers corresponding to the binary numbers X0XXXX0X
        (X is 1 or 0).
        '''
        return self.visa.ask('*STB?')
    
    def tst(self) -> int:
        '''
        (IEEE 488.2) 
        Perform a self-test and then return the seilf-test results.
        '''
        return self.visa.ask('*TST?')

    def wai(self):
        '''
        (IEEE 488.2)
        Wait for the operation to finish.
        '''
        self.visa.write('*WAI')
    


class _Screenshot:
    def screenshot(self, filename = None, format='png'):
        '''
        Downloads a screenshot from the oscilloscope.

        Args:
            filename (str): The name of the image file.  The appropriate
                extension should be included (i.e. jpg, png, bmp or tif).
            type (str): The format image that should be downloaded.  Options
                are 'jpeg, 'png', 'bmp8', 'bmp24' and 'tiff'.  It appears that
                'jpeg' takes <3sec to download while all the other formats take
                <0.5sec.  Default is 'png'.
        '''

        assert format in ('jpeg', 'png', 'bmp8', 'bmp24', 'tiff')

        #Due to the up to 3s delay, we are setting timeout to None for this operation only
        oldTimeout = self.visa_resource.timeout
        self.visa_resource.timeout = None

        raw_img = self.visa.ask_raw(':disp:data? on,off,%s' % format, 3850780)[11:-4]

        self.visa_resource.timeout = oldTimeout

        if filename:
            try:
                os.remove(filename)
            except OSError:
                pass
            with open(filename, 'wb') as fs:
                fs.write(raw_img)

        return raw_img


# CURSor Commands
# The :CURSor commands are used to measure the X-axis value (such as time) and Y-axis value (such as
# voltage) of the waveform displayed on the screen.
# Command List:
#  :CURSor:MODE
#  :CURSor:MANual
#  :CURSor:TRACk
#  :CURSor:AUTO
#  :CURSor:XY

# CURSor:MANual
# Command List:
#  :CURSor:MANual:TYPE
#  :CURSor:MANual:SOURce
#  :CURSor:MANual:TUNit
#  :CURSor:MANual:VUNit
#  :CURSor:MANual:AX
#  :CURSor:MANual:BX
#  :CURSor:MANual:AY
#  :CURSor:MANual:BY
#  :CURSor:MANual:AXValue?
#  :CURSor:MANual:AYValue?
#  :CURSor:MANual:BXValue?
#  :CURSor:MANual:BYValue?
#  :CURSor:MANual:XDELta?
#  :CURSor:MANual:IXDELta?
#  :CURSor:MANual:YDELta?
# :CURSor:MANual:TYPE

# :CURSor:TRACk
# Command List:
#  :CURSor:TRACk:SOURce1
#  :CURSor:TRACk:SOURce2
#  :CURSor:TRACk:AX
#  :CURSor:TRACk:BX
#  :CURSor:TRACk:AY?
#  :CURSor:TRACk:BY?
#  :CURSor:TRACk:AXValue?
#  :CURSor:TRACk:AYValue?
#  :CURSor:TRACk:BXValue?
#  :CURSor:TRACk:BYValue?
#  :CURSor:TRACk:XDELta?
#  :CURSor:TRACk:YDELta?
#  :CURSor:TRACk:IXDELTA?

# :CURSor:AUTO
# Command List:
#  :CURSor:AUTO:ITEM
#  :CURSor:AUTO:AX?
#  :CURSor:AUTO:BX?
#  :CURSor:AUTO:AY?
#  :CURSor:AUTO:BY?
#  :CURSor:AUTO:AXValue?
#  :CURSor:AUTO:AYValue?
#  :CURSor:AUTO:BXValue?
#  :CURSor:AUTO:BYValue?

# DECoder Commands

# :MATH Commands

# MASK commands


































# if __name__ == "__main__":
#     rm = _visa.ResourceManager()
#     print(rm.list_resources())
#     visa_resource = rm.open_resource(rm.list_resources()[0])
#     scope = Rigol_ds1000z(visa_resource)
#     print(scope.idn())
