from grader import ARM32Grader, MaximumCountFilter

from unicorn.arm_const import *

import random


class Grader(ARM32Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            MaximumCountFilter(11)
        )

        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()

            if random.random() < 0.8:
                r1 = random.randint(0, 7)
            else:
                r1 = random.randint(0, 0xffffffff)

            uc.reg_write(UC_ARM_REG_R1, r1)

            Grader.run_unicorn(code, uc)
            
            expected = [0x17, 0x60, 0xfa, 0xd0, 0xb0, 0xad, 0xed, 0x50][min(r1, 7)]

            if uc.reg_read(UC_ARM_REG_R0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", f"r1: 0x{r1:08x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]
