from grader import ARM64Grader, MaximumCountFilter

from unicorn.arm64_const import *


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            MaximumCountFilter(5)
        )

        uc = Grader.setup_unicorn()
        
        uc.reg_write(UC_ARM64_REG_X0, 0x20000)
        
        Grader.run_unicorn(code, uc)
        
        solved = uc.mem_read(0x20000, 16) == bytes(range(16))

        return solved, [
            ("Registers", Grader.register_snapshot(uc)),
            ("Memory", Grader.memory_snapshot(uc, 0x20000, 0x20010))
        ]
