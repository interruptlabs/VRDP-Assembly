from grader import ARM64Grader, MaximumCountFilter

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)
        
        Grader.filter(
            code,
            MaximumCountFilter(9)
        )
        
        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()

            varint_int_ = random.randint(0, 2**random.randint(1, 64) - 1)

            varint_int = (varint_int_ >> 1) ^ (-(varint_int_ & 1))
            varint_int = int.from_bytes(varint_int.to_bytes(8, "little", signed=True), "little", signed=False)

            varint_bytes = bytearray()
            while varint_int_ > 0x7f:
                varint_bytes.append(varint_int_ & 0x7f | 0x80)
                varint_int_ >>= 7
            varint_bytes.append(varint_int_)
            varint_bytes = bytes(varint_bytes)

            uc.mem_write(0x20000, varint_bytes)
            uc.reg_write(UC_ARM64_REG_X1, 0x20000)
        
            Grader.run_unicorn(code, uc)

            if uc.reg_read(UC_ARM64_REG_X0) != varint_int:
                solved = False
                break

        return solved, [
            ("Inputs", f"[0x20000]: {varint_bytes.hex()}"),
            ("Registers", Grader.register_snapshot(uc)),
            ("Memory", Grader.memory_snapshot(uc, 0x20000, 0x20010))
        ]
