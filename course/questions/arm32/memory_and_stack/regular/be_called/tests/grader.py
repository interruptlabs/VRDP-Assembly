from grader import ARM32Grader

from unicorn.arm_const import *

import random


class Grader(ARM32Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        pre = """
            bl be_called
            b end
        """

        post = """
        call_me_1:
            ldm sp, {r4, r5, r6}

            add r1, r1, r2, lsl #1

            lsl r3, r3, #2
            add r3, r3, r4, lsl #3

            lsl r5, r5, #4

            lsl r6, r6, #5

            stm r0, {r1, r3, r5, r6}

            bx lr

        call_me_2:
            add r0, r0, r1, lsl #1
            add r0, r0, r2, lsl #2
            add r0, r0, r3, lsl #3
            bx lr

            mov r0, #0
        end:
        """

        code = Grader.assemble(pre + answer + post)

        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()

            inputs = [random.randint(0, 0xff) for _ in range(6)]

            uc.reg_write(UC_ARM_REG_R0, inputs[0])
            uc.reg_write(UC_ARM_REG_R1, inputs[1])
            uc.reg_write(UC_ARM_REG_R2, inputs[2])
            uc.reg_write(UC_ARM_REG_R3, inputs[3])
            
            uc.reg_write(UC_ARM_REG_SP, uc.reg_read(UC_ARM_REG_SP) - 8)
            uc.mem_write(uc.reg_read(UC_ARM_REG_SP), inputs[4].to_bytes(4, "little"))
            uc.mem_write(uc.reg_read(UC_ARM_REG_SP) + 4, inputs[5].to_bytes(4, "little"))

            Grader.run_unicorn(code, uc)

            expected = (
                ((
                    (inputs[3] << 0) +
                    (inputs[2] << 1)
                ) << 3) +
                ((
                    (inputs[1] << 2) +
                    (inputs[0] << 3)
                ) << 2) +
                ((
                    (inputs[4] << 4)
                ) << 1)  +
                ((
                    (inputs[5] << 5)
                ) << 0)
            )

            if uc.reg_read(UC_ARM_REG_R0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", ", ".join(f"0x{i:02x}" for i in inputs)),
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
