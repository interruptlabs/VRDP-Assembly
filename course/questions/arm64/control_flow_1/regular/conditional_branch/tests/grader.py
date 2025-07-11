from grader import ARM64Grader

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)
    
        solved = True
        for _ in range(10):
            uc = Grader.setup_unicorn()
            
            x1 = random.randint(1, 200)

            uc.reg_write(UC_ARM64_REG_X1, x1)
            
            Grader.run_unicorn(code, uc)

            expected = 1 if x1 > 100 else 0
            
            if expected != uc.reg_read(UC_ARM64_REG_X0):
                solved = False
                break

        return solved, [
            ("Inputs", f"x1: 0x{x1:016x}"),
            ("Registers", Grader.register_snapshot(uc))
        ]
