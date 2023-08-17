from enum import auto
from strenum import StrEnum


class MyStrEnum(StrEnum):
    VAL1 = auto()
    VAL2 = auto()
    VAL3 = auto()
    VAL4 = auto()


def my_method(val:MyStrEnum) -> MyStrEnum:
    if (val not in MyStrEnum):
        print(f"{val} is not in MyStrEnum")
    return val

def my_method2(val:MyStrEnum):
    print(val)

def class_has_value(test_value, in_class) -> bool:
    values = set(item.value for item in in_class)
    return test_value in values

for val in MyStrEnum:
    print(val)
    # print(type(val))

my1 = my_method(MyStrEnum.VAL1)
print(my1)

my_method2("NO_VAL")

if class_has_value("VAL2", MyStrEnum):
    print("VAL2 is in MyStrEnum")
else:
    print("VAL2 is NOT in MyStrEnum")

if class_has_value("VAL99", MyStrEnum):
    print("VAL99 is in MyStrEnum")
else:
    print("VAL99 is NOT in MyStrEnum")

try:
    MyStrEnum.VAL99
    print("VAL99 is in MyStrEnum")
except:
    print("VAL99 is NOT in MyStrEnum")



class Outer(object):

    def createInner(self):
        return Outer.Inner(self)

    def somemethod(self):
        print("somemethod")

    def anothermethod(self):
        print("anothermethod")

    class Inner(object):
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.outer_instance.somemethod()

        def inner_method(self):
            self.outer_instance.anothermethod()

myOuter = Outer()
myOuter.createInner()
# myOuter.Inner.inner_method() # ??