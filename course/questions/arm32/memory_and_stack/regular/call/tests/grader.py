from grader import ARM32Grader

from unicorn.arm_const import *


class Grader(ARM32Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        post = """
            b end

        call_me:
            add r0, r0, r1, lsl #1
            add r0, r0, r2, lsl #2
            add r0, r0, r3, lsl #3
            ldr r12, [sp]
            add r0, r0, r12, lsl #4
            ldr r12, [sp, #4]
            add r0, r0, r12, lsl #5
            bx lr

            mov r4, #0
        end:
        """

        code = Grader.assemble(answer + post)

        uc = Grader.setup_unicorn()

        Grader.run_unicorn(code, uc)

        solved = uc.reg_read(UC_ARM_REG_R4) == (
            (0xc0 << 0) +
            (0xff << 1) +
            (0xee << 2) +
            (0x15 << 3) +
            (0xba << 4) +
            (0xad << 5)
        )

        return solved, [
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
