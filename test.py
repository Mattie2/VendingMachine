from abc import abstractmethod
# from abstract import OnePence


class A:
    instances = []
    @abstractmethod
    def __init__(self):
        self.__class__.instances.append(self)

    @classmethod
    def get_instances(self):
        return self.instances

    def add_valid(self):
        self.instances.append(self)

a = A()
b=A()

# print(a.instances)
# print(a.get_instances())

# from abstract import *

# VALID_CASH = [
#     OnePence,
#     TwoPence,
#     FivePence,
#     TenPence,
#     TwentyPence,
#     FiftyPence,
#     OnePound,
#     TwoPounds,
#     FivePounds,
#     TenPounds,
#     TwentyPounds,
#     FiftyPounds
# ]

from coin import *

onep = Cash(0.01)
twop = Cash(0.01)

print(onep==twop)