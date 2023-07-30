from rigol_visa import Rigol_visa
from rigol_ds1000z_acquire import Rigol_ds1000z_Acquire
from rigol_ds1000z_channel import Rigol_ds1000z_Channel
from rigol_ds1000z_measure import Rigol_ds1000z_Measure
from rigol_ds1000z_trigger import Rigol_ds1000z_Trigger

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
        self.measure = Rigol_ds1000z_Measure(visa_resource)

       

    def __getitem__(self, i):
        assert 1 <= i <= 4, 'Not a valid channel.'
        return self._channels[i-1]

    def __len__(self):
        return len(self._channels)

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
    


# DECoder Commands

# :MATH Commands

# MASK commands


































# if __name__ == "__main__":
#     rm = _visa.ResourceManager()
#     print(rm.list_resources())
#     visa_resource = rm.open_resource(rm.list_resources()[0])
#     scope = Rigol_ds1000z(visa_resource)
#     print(scope.idn())
