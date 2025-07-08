from grader import ARM64Grader, AllowOpcodesFilter, DenyOpcodesFilter, AllowOperandTypesFilter, MaximumCountFilter

from capstone import CS_OP_REG
from unicorn.arm64_const import *


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            AllowOpcodesFilter("add", "sub", "mul"),
            MaximumCountFilter(3)
        )

        uc = Grader.setup_unicorn()
        
        Grader.run_unicorn(code, uc)
        
        solved = uc.reg_read(UC_ARM64_REG_X0) == 999983

        return solved, [
            ("Registers", Grader.register_snapshot(uc))
        ]
