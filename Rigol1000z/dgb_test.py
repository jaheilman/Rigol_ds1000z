# import rigol_ds1000z as dso

# mydso = dso.Rigol_ds1000z()
# mydso.acquire.type

chan = 2
bw = 'OFF'
print(f':CHAN{chan}:BWLimit {bw}')

i=3
print(f'Format math {1+2*i}')

class Comms:
  def __init__(self, socket):
    self.socket = socket
  def printSocket(self):
    print(self.socket)

class Device(Comms):
  def __init__(self, socket):
    super().__init__(socket)
    self.fcn1 = Function("meas1")
    self.fcn2 = Function("meas2")

class Function(Device):
  def __init__(self, function):
    self.function = function
  def printFcn(self):
    print(self.function)
  def printFcnSocket(self):
    # print(super().printSocket())
    print(self.printSocket())

myDev = Device(99)
myDev.printSocket()
myDev.fcn1.printFcn()
# myDev.fcn2.printFcnSocket()

x = False
z = 1 if x else 0

print(z)