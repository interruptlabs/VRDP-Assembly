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

            x1 = random.randint(1, 1000000)
            x2 = random.randint(1, 1000)
            
            uc.reg_write(UC_ARM64_REG_X1, x1)
            uc.reg_write(UC_ARM64_REG_X2, x2)
            
            Grader.run_unicorn(code, uc)
            
            if uc.reg_read(UC_ARM64_REG_X0) != x1 % x2:
                solved = False
                break

        return solved, [
            ("Inputs", f"x1: 0x{x1:016x}\nx2: 0x{x2:016x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]
