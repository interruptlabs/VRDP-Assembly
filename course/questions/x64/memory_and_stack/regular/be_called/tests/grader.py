from grader import X64Grader

from unicorn.x86_const import *

import random


class Grader(X64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        pre = """
            call be_called
            jmp end_c1a99e2f
        """

        post = """
        call_me:
            shl rsi, 1
            add rdi, rsi
            shl rdx, 2
            add rdi, rdx
            shl rcx, 3
            add rdi, rcx
            mov rax, rdi
            ret

            mov rax, 0
        end_c1a99e2f:
        """

        code = Grader.assemble(pre + answer + post)

        solved = True
        for _ in range(16):
            uc = Grader.setup_unicorn()

            inputs = [random.randint(0, 0xff) for _ in range(4)]

            uc.reg_write(UC_X86_REG_RDI, inputs[0])
            uc.reg_write(UC_X86_REG_RSI, inputs[1])
            uc.reg_write(UC_X86_REG_RDX, inputs[2])
            uc.reg_write(UC_X86_REG_RCX, inputs[3])

            Grader.run_unicorn(code, uc)

            a, b, c, d = inputs
            expected = (a + (b << 1) + (c << 2) + (d << 3)) * a

            if uc.reg_read(UC_X86_REG_RAX) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", ", ".join(f"0x{i:02x}" for i in inputs)),
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
