from grader import ARM64Grader

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        pre = """
            bl be_called
            b end_c1a99e2f
        """

        post = """
        call_me:
            lsl x1, x1, #1
            add x0, x0, x1
            lsl x2, x2, #2
            add x0, x0, x2
            lsl x3, x3, #3
            add x0, x0, x3
            ret

            mov x0, #0
        end_c1a99e2f:
        """

        code = Grader.assemble(pre + answer + post)

        solved = True
        for _ in range(16):
            uc = Grader.setup_unicorn()

            inputs = [random.randint(0, 0xff) for _ in range(4)]

            uc.reg_write(UC_ARM64_REG_X0, inputs[0])
            uc.reg_write(UC_ARM64_REG_X1, inputs[1])
            uc.reg_write(UC_ARM64_REG_X2, inputs[2])
            uc.reg_write(UC_ARM64_REG_X3, inputs[3])

            Grader.run_unicorn(code, uc)

            a, b, c, d = inputs
            expected = (a + (b << 1) + (c << 2) + (d << 3)) + 1

            if uc.reg_read(UC_ARM64_REG_X0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", ", ".join(f"0x{i:02x}" for i in inputs)),
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
