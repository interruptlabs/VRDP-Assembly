from grader import ARM32Grader, AllowOpcodesFilter, DenyOpcodesFilter, AllowOperandTypesFilter, MaximumCountFilter

from capstone import CS_OP_REG
from unicorn.arm_const import *


class Grader(ARM32Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            AllowOpcodesFilter("movw", "movt"),
            MaximumCountFilter(2)
        )

        uc = Grader.setup_unicorn()
        
        Grader.run_unicorn(code, uc)
        
        solved = uc.reg_read(UC_ARM_REG_R0) == 0xdeadbeef

        return solved, [
            ("Registers", Grader.register_snapshot(uc))
        ]
