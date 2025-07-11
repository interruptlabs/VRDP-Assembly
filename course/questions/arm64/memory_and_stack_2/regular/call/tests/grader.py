from grader import ARM64Grader

from unicorn.arm64_const import *


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        post = """
            b end

        call_me:
            ldp x8, x9, [sp]
            add x0, x0, x1, lsl #1
            add x0, x0, x2, lsl #2
            add x0, x0, x3, lsl #3
            add x0, x0, x4, lsl #4
            add x0, x0, x5, lsl #5
            add x0, x0, x6, lsl #6
            add x0, x0, x7, lsl #7
            add x0, x0, x8, lsl #8
            add x0, x0, x9, lsl #9
            ret

            mov x7, #0
        end:
        """

        code = Grader.assemble(answer + post)

        uc = Grader.setup_unicorn()
        
        Grader.run_unicorn(code, uc)
        
        solved = uc.reg_read(UC_ARM64_REG_X7) == (
            (0xde << 0) +
            (0xad << 1) +
            (0xbe << 2) +
            (0xef << 3) +
            (0xc0 << 4) +
            (0xff << 5) +
            (0xee << 6) +
            (0x15 << 7) +
            (0xba << 8) +
            (0xad << 9)
        )

        return solved, [
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
