from grader import ARM64Grader, MaximumCountFilter

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            MaximumCountFilter(7)
        )

        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()
            
            x0 = random.randint(0, 0xffffffffffffffff)
            x1 = random.randint(3, 1000)

            uc.reg_write(UC_ARM64_REG_X0, x0)
            uc.reg_write(UC_ARM64_REG_X1, x1)
            
            Grader.run_unicorn(code, uc)

            expected = int(not any(x1 % i == 0 for i in range(2, x1)))
            
            if uc.reg_read(UC_ARM64_REG_X0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", f"x0: 0x{x0:016x}\nx1: 0x{x1:016x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]
