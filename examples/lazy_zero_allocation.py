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


lazy_zero = capnp.LazyZeroSegmentAlloc(enableLazyZero=True, skipLazyZeroTypes={capnp.types.Data})
builder_options=capnp.BuilderOptions(lazyZeroSegmentAlloc=lazy_zero)

# message creation method 1
person = addressbook_capnp.Person.new_message(allocate_seg_callable=Allocator(), builder_options=builder_options)
print(person.name) # guaranteed empty string
person.name = "test name 1"
print(person.name)
person.init("extraData", 100) # random dirty bytes
print(bytes(person.extraData))
print()

# message creation method 2
builder = capnp._PyCustomMessageBuilder(allocate_seg_callable=Allocator())
builder.set_options(builder_options)
person = builder.init_root(addressbook_capnp.Person)
print(person.name) # guaranteed empty string
person.name = "test name 2"
print(person.name)
person.init("extraData", 100) # random dirty bytes
print(bytes(person.extraData))
builder.get_options()
print(len(builder.get_options().lazyZeroSegmentAlloc.skipLazyZeroTypes)) # return a set of length 1
