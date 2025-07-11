from grader import ARM64Grader

from unicorn.arm64_const import *

import random


class Grader(ARM64Grader):
    @staticmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        pre = """
            bl sort
            b end
        """

        post = """
        end:
        """

        code = Grader.assemble(pre + answer + post)

        solved = True
        for length in map(lambda x: 2 ** x, range(1, 10)):
            uc = Grader.setup_unicorn()

            array = [random.randint(0, 0xffffffffffffffff) for _ in range(length)]

            array_ptr = Grader.DATA_BASE
            scratch_ptr = Grader.DATA_BASE + length * 8

            uc.mem_write(array_ptr, b"".join(i.to_bytes(8, "little") for i in array))

            uc.reg_write(UC_ARM64_REG_X0, array_ptr)
            uc.reg_write(UC_ARM64_REG_X1, length)
            uc.reg_write(UC_ARM64_REG_X2, scratch_ptr)

            Grader.run_unicorn(code, uc)

            result = uc.mem_read(array_ptr, length * 8)
            result = [int.from_bytes(result[i:i+8], "little") for i in range(0, len(result), 8)]
        
            if result != sorted(array):
                solved = False
                break

        return solved, [
            ("Inputs", f"""array: 0x{array_ptr:016x}\nlength: {length}\nscratch: 0x{scratch_ptr:016x}\n[array]: {", ".join(f"0x{i:016x}" for i in array)}"""),
            ("Registers", Grader.register_snapshot(uc)),
            ("Memory", Grader.memory_snapshot(uc, array_ptr, array_ptr + length * 16)),
            ("Stack", Grader.stack_snapshot(uc))
        ]
