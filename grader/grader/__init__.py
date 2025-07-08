from abc import ABC, abstractmethod
from typing import ClassVar

from capstone import Cs, CsInsn, CS_ARCH_ARM64, CS_MODE_ARM, CS_MODE_LITTLE_ENDIAN
from keystone import Ks, KS_ARCH_ARM64, KS_MODE_ARM, KS_MODE_LITTLE_ENDIAN
from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM
from unicorn.arm64_const import *

class Filter(ABC):
    @abstractmethod
    def filter(self, instruction: CsInsn, count: int) -> bool:
        pass


class AllowOpcodesFilter(Filter):
    opcodes: set[str]


    def __init__(self, *opcodes: str) -> None:
        self.opcodes = set(opcodes)


    def filter(self, instruction: CsInsn, count: int) -> None:
        if instruction.mnemonic not in self.opcodes:
            raise ValueError(f"Disallowed instruction (opcode): {instruction.mnemonic} {instruction.op_str}.")


class DenyOpcodesFilter(Filter):
    opcodes: set[str]


    def __init__(self, *opcodes: str) -> None:
        self.opcodes = set(opcodes)


    def filter(self, instruction: CsInsn, count: int) -> None:
        if instruction.mnemonic in self.opcodes:
            raise ValueError(f"Disallowed instruction (opcode): {instruction.mnemonic} {instruction.op_str}.")


class AllowOperandTypesFilter(Filter):
    operand_types: set[int]


    def __init__(self, *operand_types: int) -> None:
        self.operand_types = set(operand_types)


    def filter(self, instruction: CsInsn, count: int) -> None:
        for operand in instruction.operands:
            if operand.type not in self.operand_types:
                raise ValueError(f"Disallowed instruction (operand type): {instruction.mnemonic} {instruction.op_str}.")


class MaximumCountFilter(Filter):
    maximum_count: int


    def __init__(self, maximum_count: int) -> None:
        self.maximum_count = maximum_count


    def filter(self, instruction: CsInsn, count: int) -> None:
        if count > self.maximum_count:
            raise ValueError(f"Too many instructions: {count}.")
    

class GenericGrader(ABC):
    @staticmethod
    @abstractmethod
    def grade(answer: str) -> tuple[bool, list[tuple[str, str]]]:
        pass


class ARM64Grader(GenericGrader, ABC):
    SECTION_SIZE: ClassVar[int] = 0x10000
    TEXT_BASE: ClassVar[int] = 1 * SECTION_SIZE
    DATA_BASE: ClassVar[int] = 2 * SECTION_SIZE
    STACK_BASE: ClassVar[int] = 3 * SECTION_SIZE
    UNICORN_TIMEOUT: ClassVar[int] = 5000
    UNICORN_COUNT: ClassVar[int] = 1000000
    STACK_SNAPSHOT_DEPTH: ClassVar[int] = 32


    @staticmethod
    def assemble(assembly: str) -> bytes:
        ks = Ks(
            KS_ARCH_ARM64,
            KS_MODE_LITTLE_ENDIAN
        )

        return ks.asm(assembly, addr=ARM64Grader.TEXT_BASE, as_bytes=True)[0]


    @staticmethod
    def filter(code: bytes, *filters: Filter) -> None:
        cs = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN | CS_MODE_ARM)
        cs.detail = True

        count = 0
        for instruction in cs.disasm(code, ARM64Grader.TEXT_BASE):
            count += 1

            for filter in filters:
                filter.filter(instruction, count)
    

    @staticmethod
    def setup_unicorn() -> Uc:
        uc = Uc(UC_ARCH_ARM64, UC_MODE_ARM)

        uc.mem_map(ARM64Grader.TEXT_BASE, ARM64Grader.SECTION_SIZE)
        uc.mem_map(ARM64Grader.DATA_BASE, ARM64Grader.SECTION_SIZE)
        uc.mem_map(ARM64Grader.STACK_BASE, ARM64Grader.SECTION_SIZE)

        uc.reg_write(UC_ARM64_REG_PC, ARM64Grader.TEXT_BASE)
        uc.reg_write(
            UC_ARM64_REG_SP, ARM64Grader.STACK_BASE + ARM64Grader.SECTION_SIZE
        )

        return uc

    @staticmethod
    def run_unicorn(code: bytes, uc: Uc) -> None:
        if len(code) > ARM64Grader.SECTION_SIZE:
            raise ValueError(f"Code is too large: {len(code)}.")

        uc.mem_write(ARM64Grader.TEXT_BASE, code)

        uc.emu_start(
            ARM64Grader.TEXT_BASE,
            ARM64Grader.TEXT_BASE + len(code),
            timeout=ARM64Grader.UNICORN_TIMEOUT,
            count=ARM64Grader.UNICORN_COUNT,
        )


    @staticmethod
    def register_snapshot(uc: Uc) -> str:
        pc_value = uc.reg_read(UC_ARM64_REG_PC)
        fp_value = uc.reg_read(UC_ARM64_REG_X29)
        lr_value = uc.reg_read(UC_ARM64_REG_X30)
        sp_value = uc.reg_read(UC_ARM64_REG_SP)

        lines = [
            f"pc:       0x{pc_value:016x}",
            f"lr (x30): 0x{lr_value:016x}",
            f"sp;     : 0x{sp_value:016x}",
            f"fp (x29): 0x{fp_value:016x}",
        ]

        nzcv = uc.reg_read(UC_ARM64_REG_NZCV)
        n_flag = "N" if nzcv & (1 << 31) else "n"
        z_flag = "Z" if nzcv & (1 << 30) else "z"
        c_flag = "C" if nzcv & (1 << 29) else "c"
        v_flag = "V" if nzcv & (1 << 28) else "v"
        lines.append(f"flags:    {n_flag}{z_flag}{c_flag}{v_flag}")

        x_registers = [
            UC_ARM64_REG_X0,
            UC_ARM64_REG_X1,
            UC_ARM64_REG_X2,
            UC_ARM64_REG_X3,
            UC_ARM64_REG_X4,
            UC_ARM64_REG_X5,
            UC_ARM64_REG_X6,
            UC_ARM64_REG_X7,
            UC_ARM64_REG_X8,
            UC_ARM64_REG_X9,
            UC_ARM64_REG_X10,
            UC_ARM64_REG_X11,
            UC_ARM64_REG_X12,
            UC_ARM64_REG_X13,
            UC_ARM64_REG_X14,
            UC_ARM64_REG_X15,
            UC_ARM64_REG_X16,
            UC_ARM64_REG_X17,
            UC_ARM64_REG_X18,
            UC_ARM64_REG_X19,
            UC_ARM64_REG_X20,
            UC_ARM64_REG_X21,
            UC_ARM64_REG_X22,
            UC_ARM64_REG_X23,
            UC_ARM64_REG_X24,
            UC_ARM64_REG_X25,
            UC_ARM64_REG_X26,
            UC_ARM64_REG_X27,
            UC_ARM64_REG_X28,
        ]

        for i in range(0, 29, 4):
            line_parts = []
            for j in range(4):
                register_index = i + j
                if register_index < 29:
                    register_value = uc.reg_read(x_registers[register_index])
                    line_parts.append(
                        f"""x{register_index}: {" " if register_index < 10 else ""} 0x{register_value:016x}"""
                    )
            lines.append("  ".join(line_parts))

        return "\n".join(lines)


    @staticmethod
    def stack_snapshot(uc: Uc) -> str:
        sp_value = uc.reg_read(UC_ARM64_REG_SP)
        fp_value = uc.reg_read(UC_ARM64_REG_X29)

        if sp_value == ARM64Grader.STACK_BASE + ARM64Grader.SECTION_SIZE:
            return "Stack is empty."

        if not (
            ARM64Grader.STACK_BASE
            <= sp_value
            < ARM64Grader.STACK_BASE + ARM64Grader.SECTION_SIZE
        ):
            return f"Stack is out of bounds: 0x{sp_value:016x}."

        if sp_value & 0x7 != 0:
            return f"Stack is not aligned: 0x{sp_value:016x}."

        lines = []

        for i in range(ARM64Grader.STACK_SNAPSHOT_DEPTH):
            offset = i * 8
            address = sp_value + offset

            value = int.from_bytes(uc.mem_read(address, 8), "little")
            line = f"sp + 0x{offset:02x}: 0x{value:016x}"

            if address == fp_value:
                line += " <- fp"

            lines.append(line)

        return "\n".join(lines)


    @staticmethod
    def memory_snapshot(uc: Uc, start_address: int, end_address: int) -> str:
        lines = []
        current_address = start_address & ~0xF
        while current_address < end_address:
            data = uc.mem_read(current_address, 16)

            line = []
            for i in range(16):
                if start_address <= current_address + i < end_address:
                    line.append(f"{data[i]:02x}")
                else:
                    line.append("  ")

            hex_line = f"""{" ".join(line[:8])}  {" ".join(line[8:])}"""

            line = f"0x{current_address:016x}: {hex_line}"
            lines.append(line)

            current_address += 16

        return "\n".join(lines)
