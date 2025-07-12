from grader import THUMB32Grader, MaximumCountFilter

import random
from unicorn.arm_const import *


class Grader(THUMB32Grader):
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

            if random.random() < 0.8:
                r1 = random.randint(0, 0xffffffff)
            else:
                r1 = 42

            uc.reg_write(UC_ARM_REG_R1, r1)

            Grader.run_unicorn(code, uc)

            expected = 0xdeadbeef if r1 == 42 else 0xbaadc0de

            if uc.reg_read(UC_ARM_REG_R0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", f"r1: 0x{r1:08x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]