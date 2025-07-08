from grader import ARM64Grader, AllowOpcodesFilter, DenyOpcodesFilter, AllowOperandTypesFilter, MaximumCountFilter

from capstone import CS_OP_REG
from unicorn.arm64_const import *


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            # TODO
        )

        uc = Grader.setup_unicorn()
        
        # TODO
        
        Grader.run_unicorn(code, uc)
        
        # TODO

        return solved, [
            ("Registers", Grader.register_snapshot(uc))
        ]
