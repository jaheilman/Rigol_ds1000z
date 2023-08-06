from rigol_visa import Rigol_visa
import os

class Rigol_ds1000z_Screenshot:
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        self.visa = Rigol_visa(visa_resource)


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
