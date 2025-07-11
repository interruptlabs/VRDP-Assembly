from grader import ARM64Grader

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        pre = """
            bl be_called
            b end
        """

        post = """
        call_me_1:
            ldr x9, [sp]

            add x0, x0, x1, lsl #1
            add x0, x0, x2, lsl #2

            lsl x3, x3, #3
            add x3, x3, x4, lsl #4
            add x3, x3, x5, lsl #5

            lsl x6, x6, #6
            add x6, x6, x7, lsl #7
            add x6, x6, x9, lsl #8

            stp x0, x3, [x8]
            str x6, [x8, #16]

            ret

        call_me_2:
            add x0, x0, x1, lsl #1
            add x0, x0, x2, lsl #2
            ret

            mov x0, #0
        end:
        """
        
        code = Grader.assemble(pre + answer + post)

        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()

            inputs = [random.randint(0, 0xff) for _ in range(9)]

            uc.reg_write(UC_ARM64_REG_X0, inputs[0])
            uc.reg_write(UC_ARM64_REG_X1, inputs[1])
            uc.reg_write(UC_ARM64_REG_X2, inputs[2])
            uc.reg_write(UC_ARM64_REG_X3, inputs[3])
            uc.reg_write(UC_ARM64_REG_X4, inputs[4])
            uc.reg_write(UC_ARM64_REG_X5, inputs[5])
            uc.reg_write(UC_ARM64_REG_X6, inputs[6])
            uc.reg_write(UC_ARM64_REG_X7, inputs[7])
            
            uc.reg_write(UC_ARM64_REG_SP, uc.reg_read(UC_ARM64_REG_SP) - 16)
            uc.mem_write(uc.reg_read(UC_ARM64_REG_SP), inputs[8].to_bytes(8, "little"))

            Grader.run_unicorn(code, uc)

            expected = (
                ((
                    (inputs[0] << 8) +
                    (inputs[1] << 7) +
                    (inputs[2] << 6)
                ) << 1) +
                ((
                    (inputs[3] << 5) +
                    (inputs[4] << 4) +
                    (inputs[5] << 3)
                ) << 0) +
                ((
                    (inputs[6] << 2) +
                    (inputs[7] << 1) +
                    (inputs[8] << 0)
                ) << 2)
            )

            if uc.reg_read(UC_ARM64_REG_X0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", ", ".join(f"0x{i:02x}" for i in inputs)),
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
