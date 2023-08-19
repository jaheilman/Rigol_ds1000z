from .rigol_visa import Rigol_visa
from .rigol_ds1000z_constants import DisplayTypes, DisplayGradingTime, DisplayGridTypes
import os

class Rigol_ds1000z_Screenshot:
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)

    def clear(self):
        '''
        :DISPlay:CLEar
        Clear all the waveforms on the screen.
        '''
        self.visa.write(f':DISPlay:CLEar')
        return
    
    def data(self, color, invert, format):
        '''
        :DISPlay:DATA? [<color>,<invert>,<format>]
        Read the data stream of the image currently displayed on the screen and set the color,
        invert display, and format of the image acquired.

        <color> Bool {ON|OFF}           default: ON
        <invert> Bool {{1|ON}|{0|OFF}}  default: 0|OFF
        <format> Discrete {BMP24|BMP8|PNG|JPEG|TIFF} default: BMP24
        '''
        self.visa.write(f':DISPlay:DATA? {color},{invert},{format}')
        return
    
    @property
    def type(self) -> DisplayTypes:
        '''
        :DISP:TYPE
        Set or query the display mode of the waveform on the screen; vectors or dots
        '''
        return  (self.visa.write(f':DISPlay:TYPE?'))
    @type.setter
    def type(self, display_type:DisplayTypes):
        self.visa.write(f':DISP:TYPE {display_type}')
        return

    @property
    def grading_time(self) -> DisplayTypes:
        '''
        :DISPlay:GRADing:TIME
        Set or query the persistence time. The default unit is s.

        <time> Discrete {MIN|0.1|0.2|0.5|1|5|10|INFinite}
        '''
        return  (self.visa.write(f':DISPlay:GRADing:TIME?'))
    @grading_time.setter
    def grading_time(self, time:DisplayGradingTime):
        self.visa.write(f':DISPlay:GRADing:TIME {time}')
        return


    @property
    def brightness(self) -> int:
        '''
        :DISPlay:WBRightness
        Set or query the waveform brightness.

        <brightness> is an integeger between 0 and 100, default 60
        '''
        return  int(self.visa.write(f':DISPlay:WBRightness?'))
    @brightness.setter
    def brightness(self, brightness:int):
        if brightness < 0: brightness = 0
        if brightness > 100: brightness = 100
        self.visa.write(f':DISPlay:WBRightness {brightness}')
        return

    @property
    def grid_type(self) -> DisplayGridTypes:
        '''
        :DISPlay:GRID
        Set or query the grid type of screen display.

        <grid> Discrete {FULL|HALF|NONE}
        '''
        return  int(self.visa.write(f':DISPlay:GRID?'))
    @grid_type.setter
    def grid_type(self, grid:DisplayGridTypes):
        self.visa.write(f':DISPlay:GRID {grid}')
        return
    
    def grid_brightness(self) -> int:
        '''
        :DISPlay:GBRightness
        Set or query the grid brightness.

        <brightness> is an integeger between 0 and 100, default 60
        '''
        return  int(self.visa.write(f':DISPlay:GBRightness?'))
    @grid_brightness.setter
    def grid_brightness(self, brightness:int):
        if brightness < 0: brightness = 0
        if brightness > 100: brightness = 100
        self.visa.write(f':DISPlay:GBRightness {brightness}')
        return












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

        raw_img = self.visa.query_raw(':disp:data? on,off,%s' % format, 3850780)[11:-4]

        self.visa_resource.timeout = oldTimeout

        if filename:
            try:
                os.remove(filename)
            except OSError:
                pass
            with open(filename, 'wb') as fs:
                fs.write(raw_img)

        return raw_img
