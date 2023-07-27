
import pyvisa as visa

class Rigol_visa:
    def __init__(self, visa_resource):
        self.visa_resource = visa_resource
        return

    def write(self, cmd):
        self.visa_resource.write(cmd)
        return

    def read(self):
        return self.visa_resource.read().strip()

    def read_raw(self, num_bytes=-1):
        return self.visa_resource.read_raw(num_bytes)

    def ask(self, cmd):
        return self.visa_resource.query(cmd)

    def ask_raw(self, cmd, num_bytes=-1):
        self.write(cmd)
        return self.read_raw(num_bytes)

    