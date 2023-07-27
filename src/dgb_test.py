from rigol_ds1000z import Rigol_ds1000z
import pyvisa as visa

rm = visa.ResourceManager()
print(rm.list_resources())
visa_resource = rm.open_resource(rm.list_resources()[0])
mydso = Rigol_ds1000z(visa_resource)

print(mydso.idn())
print(mydso.acquire.averages)
mydso.acquire.averages=4
print(mydso.acquire.averages)

