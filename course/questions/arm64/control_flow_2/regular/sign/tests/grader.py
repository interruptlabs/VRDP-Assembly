from grader import ARM64Grader, MaximumCountFilter

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        test_code = Grader.assemble(answer)

        pre = """
            bl sign
            b end
        """

        post = """
            movz x0, #0
        end:
        """

        code = Grader.assemble(pre + answer + post)

        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()
            
            if random.random() < 0.8:
                x0_ = random.randint(-100, 100)
            else:
                x0_ = 0

            x0 = int.from_bytes(x0_.to_bytes(8, "little", signed=True), "little", signed=False)

            uc.reg_write(UC_ARM64_REG_X0, x0)
            
            Grader.run_unicorn(code, uc)

            expected = 0
            if x0_ > 0:
                expected = 1
            if x0_ < 0:
                expected = 0xffffffffffffffff
            
            if uc.reg_read(UC_ARM64_REG_X0) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", f"x0: 0x{x0:016x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]

