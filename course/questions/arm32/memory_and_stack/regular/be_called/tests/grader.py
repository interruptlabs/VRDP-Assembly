from grader import ARM32Grader

from unicorn.arm_const import *

import random


class Grader(ARM32Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        pre = """
            bl be_called
            b end_c1a99e2f
        """

        post = """
        call_me:
            lsl r1, r1, #1
            add r0, r0, r1
            lsl r2, r2, #2
            add r0, r0, r2
            lsl r3, r3, #3
            add r0, r0, r3
            bx lr

            mov r0, #0
        end_c1a99e2f:
        """

        code = Grader.assemble(pre + answer + post)

        solved = True
        for _ in range(16):
            uc = Grader.setup_unicorn()

            inputs = [random.randint(0, 0xff) for _ in range(4)]

            uc.reg_write(UC_ARM_REG_R0, inputs[0])
            uc.reg_write(UC_ARM_REG_R1, inputs[1])
            uc.reg_write(UC_ARM_REG_R2, inputs[2])
            uc.reg_write(UC_ARM_REG_R3, inputs[3])

            Grader.run_unicorn(code, uc)

            a, b, c, d = inputs
            expected = (a + (b << 1) + (c << 2) + (d << 3)) + a

            if uc.reg_read(UC_ARM_REG_R0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", ", ".join(f"0x{i:02x}" for i in inputs)),
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
