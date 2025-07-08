from grader import ARM64Grader, AllowOpcodesFilter, MaximumCountFilter

from unicorn.arm64_const import *


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        code = Grader.assemble(answer)

        Grader.filter(
            code,
            AllowOpcodesFilter("mul"),
            MaximumCountFilter(1)
        )

        uc = Grader.setup_unicorn()
        
        uc.reg_write(UC_ARM64_REG_X0, 0x1337)
        uc.reg_write(UC_ARM64_REG_X1, 0x1337)
        uc.reg_write(UC_ARM64_REG_X2, 0x1337)
        uc.reg_write(UC_ARM64_REG_X3, 0x1337)
        uc.reg_write(UC_ARM64_REG_X4, 0x1337)
        uc.reg_write(UC_ARM64_REG_X5, 0x1337)
        uc.reg_write(UC_ARM64_REG_X6, 0x1337)
        uc.reg_write(UC_ARM64_REG_X7, 0x1337)
        uc.reg_write(UC_ARM64_REG_X8, 0x1337)
        uc.reg_write(UC_ARM64_REG_X9, 0x1337)
        uc.reg_write(UC_ARM64_REG_X10, 0x1337)
        uc.reg_write(UC_ARM64_REG_X11, 0x1337)
        uc.reg_write(UC_ARM64_REG_X12, 0x1337)
        uc.reg_write(UC_ARM64_REG_X13, 0x1337)
        uc.reg_write(UC_ARM64_REG_X14, 0x1337)
        uc.reg_write(UC_ARM64_REG_X15, 0x1337)
        uc.reg_write(UC_ARM64_REG_X16, 0x1337)
        uc.reg_write(UC_ARM64_REG_X17, 0x1337)
        uc.reg_write(UC_ARM64_REG_X18, 0x1337)
        uc.reg_write(UC_ARM64_REG_X19, 0x1337)
        uc.reg_write(UC_ARM64_REG_X20, 0x1337)
        uc.reg_write(UC_ARM64_REG_X21, 0x1337)
        uc.reg_write(UC_ARM64_REG_X22, 0x1337)
        uc.reg_write(UC_ARM64_REG_X23, 0x1337)
        uc.reg_write(UC_ARM64_REG_X24, 0x1337)
        uc.reg_write(UC_ARM64_REG_X25, 0x1337)
        uc.reg_write(UC_ARM64_REG_X26, 0x1337)
        uc.reg_write(UC_ARM64_REG_X27, 0x1337)
        uc.reg_write(UC_ARM64_REG_X28, 0x1337)
        uc.reg_write(UC_ARM64_REG_X29, 0x1337)
        uc.reg_write(UC_ARM64_REG_X30, 0x1337)
        
        Grader.run_unicorn(code, uc)
        
        solved = uc.reg_read(UC_ARM64_REG_X0) == 0

        return solved, [
            ("Registers", Grader.register_snapshot(uc))
        ]
