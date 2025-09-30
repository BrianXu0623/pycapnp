import capnp
import random

import addressbook_capnp

WORD_SIZE = 8


class Allocator:
    def __init__(self):
        return

    def __call__(self, minimum_size: int) -> bytearray:
        print(minimum_size)
        # dirty the memory on purpose, to simulate reusing shared memory
        return bytearray(random.getrandbits(8) for _ in range(minimum_size * WORD_SIZE))

builder_options=capnp.BuilderOptions(lazyZeroSegment=True, skipZeroData=True)
person = addressbook_capnp.Person.new_message(allocate_seg_callable=Allocator(), builder_options=builder_options)
print(person.name)
person.name = "test name"
print(person.name)
person.init("extraData", 100)
print(bytes(person.extraData))
