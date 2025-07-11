from grader import ARM64Grader, MaximumCountFilter

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            MaximumCountFilter(3)
        )

        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()

            x1 = random.randint(0, 200)

            uc.reg_write(UC_ARM64_REG_X1, x1)
        
            Grader.run_unicorn(code, uc)
        
            if uc.reg_read(UC_ARM64_REG_X0) != (x1 < 100 and x1 % 2 == 1):
                solved = False
                break

        return solved, [
            ("Inputs", f"x1: 0x{x1:016x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]
