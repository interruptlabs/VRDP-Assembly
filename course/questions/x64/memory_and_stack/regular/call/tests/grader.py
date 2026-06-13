from grader import X64Grader

from unicorn.x86_const import *


class Grader(X64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        post = """
            jmp end

        call_me:
            shl rsi, 1
            add rdi, rsi
            shl rdx, 2
            add rdi, rdx
            shl rcx, 3
            add rdi, rcx
            shl r8, 4
            add rdi, r8
            shl r9, 5
            add rdi, r9
            mov r10, [rsp + 8]
            shl r10, 6
            add rdi, r10
            mov r11, [rsp + 16]
            shl r11, 7
            add rdi, r11
            mov rax, rdi
            ret

            mov r15, 0
        end:
        """

        code = Grader.assemble(answer + post)

        uc = Grader.setup_unicorn()

        Grader.run_unicorn(code, uc)

        solved = uc.reg_read(UC_X86_REG_R15) == (
            (0xc0 << 0) +
            (0xff << 1) +
            (0xee << 2) +
            (0x15 << 3) +
            (0xba << 4) +
            (0xad << 5) +
            (0xf0 << 6) +
            (0x0d << 7)
        )

        return solved, [
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
