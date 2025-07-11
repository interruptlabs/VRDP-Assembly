from grader import ARM64Grader, MaximumCountFilter

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            MaximumCountFilter(2)
        )

        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()
            
            while (x1 := random.randint(0, 0xffffffffffffffff)) == 0x8000000000000000:
                pass

            uc.reg_write(UC_ARM64_REG_X1, x1)
        
            Grader.run_unicorn(code, uc)

            expected = abs(int.from_bytes(x1.to_bytes(8, "big", signed=False), "big", signed=True))
        
            if uc.reg_read(UC_ARM64_REG_X0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", f"x1: 0x{x1:016x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]
