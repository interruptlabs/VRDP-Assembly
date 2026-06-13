from grader import X64Grader, AllowOpcodesFilter, DenyOpcodesFilter, AllowOperandTypesFilter, MaximumCountFilter

from capstone import CS_OP_REG
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
        call_me_1:
            shl rdx, 1
            add rsi, rdx
            shl rcx, 2
            add rsi, rcx

            shl r8, 3
            shl r9, 4
            add r8, r9
            mov r11, [rsp + 8]
            shl r11, 5
            add r8, r11

            mov r10, [rsp + 16]
            shl r10, 6
            mov r11, [rsp + 24]
            shl r11, 7
            add r10, r11
            mov r11, [rsp + 32]
            shl r11, 8
            add r10, r11

            mov [rdi], rsi
            mov [rdi + 8], r8
            mov [rdi + 16], r10

            ret

        call_me_2:
            shl rsi, 1
            add rdi, rsi
            shl rdx, 2
            add rdi, rdx
            mov rax, rdi
            ret

            mov rax, 0
        end_c1a99e2f:
        """

        code = Grader.assemble(pre + answer + post)

        solved = True
        for _ in range(16):
            uc = Grader.setup_unicorn()

            inputs = [random.randint(0, 0xff) for _ in range(9)]

            uc.reg_write(UC_X86_REG_RDI, inputs[0])
            uc.reg_write(UC_X86_REG_RSI, inputs[1])
            uc.reg_write(UC_X86_REG_RDX, inputs[2])
            uc.reg_write(UC_X86_REG_RCX, inputs[3])
            uc.reg_write(UC_X86_REG_R8, inputs[4])
            uc.reg_write(UC_X86_REG_R9, inputs[5])
            
            uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) - 32)
            uc.mem_write(uc.reg_read(UC_X86_REG_RSP), inputs[6].to_bytes(8, "little"))
            uc.mem_write(uc.reg_read(UC_X86_REG_RSP) + 8, inputs[7].to_bytes(8, "little"))
            uc.mem_write(uc.reg_read(UC_X86_REG_RSP) + 16, inputs[8].to_bytes(8, "little"))

            Grader.run_unicorn(code, uc)

            expected = (
                ((
                    (inputs[3] << 0) +
                    (inputs[2] << 1) +
                    (inputs[1] << 2)
                ) << 2) +
                ((
                    (inputs[0] << 3) +
                    (inputs[8] << 4) +
                    (inputs[7] << 5)
                ) << 1) +
                ((
                    (inputs[6] << 6) +
                    (inputs[5] << 7) +
                    (inputs[4] << 8)
                ) << 0)
            )

            if uc.reg_read(UC_X86_REG_RAX) != expected:
                solved = False
                break

        return solved, [
            ("Inputs", ", ".join(f"0x{i:02x}" for i in inputs)),
            ("Registers", Grader.register_snapshot(uc)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
