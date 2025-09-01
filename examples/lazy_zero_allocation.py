import capnp
import random

import addressbook_capnp

WORD_SIZE = 8


class Allocator:
    def __init__(self):
        return

    def __call__(self, minimum_size: int) -> bytearray:
        # dirty the memory on purpose, to simulate reusing shared memory
        return bytearray(random.getrandbits(8) for _ in range(minimum_size * WORD_SIZE))


mb = capnp._PyCustomMessageBuilder(allocate_seg_callable=Allocator(), size=1)
# set the lazy zero memory allocate options
mb.set_alloc_options(capnp.AllocateOptions(lazyZeroSegment=True, skipZeroData=True))
people = mb.init_root(addressbook_capnp.Person)
print(people.name)
people.name = "test name"
print(people.name)
people.init("extraData", 100)
print(bytes(people.extraData))
