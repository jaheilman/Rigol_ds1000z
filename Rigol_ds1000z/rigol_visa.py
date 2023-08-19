
import pyvisa as _visa


class Rigol_visa:
    # def __init__(self, visa_resource:_visa.resources.Resource): # not sure this is the right type hint
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        return

    def write(self, cmd):
        self.visa_resource.write(cmd)
        return

    def read(self):
        return self.visa_resource.read().strip()

    def read_raw(self, num_bytes:int=None):
        return self.visa_resource.read_raw(num_bytes)

    def query(self, cmd):
        return self.visa_resource.query(cmd)

    def write_read_raw(self, cmd, num_bytes:int=None):
        self.write(cmd)
        return self.read_raw(num_bytes)

    