from grader import ARM32Grader, MaximumCountFilter

from unicorn.arm_const import *

import random


class Grader(ARM32Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            MaximumCountFilter(1)
        )

        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()

            r1 = random.randint(0, 0xffffffff)
            r2 = random.randint(0, 0xffffffff)

            uc.reg_write(UC_ARM_REG_R1, r1)
            uc.reg_write(UC_ARM_REG_R2, r2)

            Grader.run_unicorn(code, uc)

            r1_ = int.from_bytes(r1.to_bytes(4, "little", signed=False), "little", signed=True)
            r2_ = int.from_bytes(r2.to_bytes(4, "little", signed=False), "little", signed=True)
            
            expected = r1_ + r2_

            if expected > 0x7fffffff:
                expected = 0x7fffffff

            if expected < -0x80000000:
                expected = -0x80000000

            expected = int.from_bytes(expected.to_bytes(4, "little", signed=True), "little", signed=False)

            if uc.reg_read(UC_ARM_REG_R0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", f"r1: 0x{r1:08x}\nr2: 0x{r2:08x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]
