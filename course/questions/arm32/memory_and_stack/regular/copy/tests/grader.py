from grader import ARM32Grader, MaximumCountFilter

from unicorn.arm_const import *


class Grader(ARM32Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            MaximumCountFilter(2)
        )

        uc = Grader.setup_unicorn()
        
        uc.mem_write(0x20000, bytes.fromhex("6e483004987aab4ba973270b35a28109"))
        uc.reg_write(UC_ARM_REG_R0, 0x20000)

        Grader.run_unicorn(code, uc)
        
        solved = uc.mem_read(0x20010, 16) == bytes.fromhex("6e483004987aab4ba973270b35a28109")

        return solved, [
            ("Registers", Grader.register_snapshot(uc)),
            ("Memory", Grader.memory_snapshot(uc, 0x20000, 0x20020))
        ]
