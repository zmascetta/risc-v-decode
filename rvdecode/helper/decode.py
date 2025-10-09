from . import errorcheck

def get_opcode(instruction):
    return instruction[25:]


def get_rs1(instruction):
    return instruction[12:17]


def get_rs2(instruction):
    return instruction[7:12]


def get_rd(instruction):
    return instruction[20:25]


def get_func3(instruction):
    return instruction[17:20]


def get_func7(instruction):
    return instruction[0:8]


def get_immediate(instruction, instruction_type):
    if instruction_type == "I-Type":
        return instruction[0:12]
    elif instruction_type == "S-Type":
        return instruction[0:8] + instruction[20:25]
    elif instruction_type == "B-Type":
        return instruction[0:0] + instruction[24:25] + instruction[1:7] + instruction[20:24] + "0"
    elif instruction_type == "U-Type":
        return instruction[0:20].ljust(32,"0")
    else:   #J-Type
        immediate = instruction[0:1] + instruction[12:20] + instruction[11:12] + instruction[1:11] + "0"
        immediate.zfill(32)
        return immediate


# Identify instruction type via opcode.
def get_instruction_type(opcode):
    if opcode == "1101111":
        return "J-Type"
    elif opcode == "1100011":
        return "B-Type"
    elif opcode == "0110011":
        return "R-Type"
    elif opcode == "0100011":
        return "S-Type"
    elif opcode in ("0110111", "0010111"):
        return "U-Type"
    elif opcode in ("0000011", "0010011", "0001111", "1110011"):
        return "I-Type"
    else:
        extra_lines = "ERROR: Opcode in instruction is not valid."
        return errorcheck.system_exit(extra_lines)


def decode_instruction(instruction):
    opcode = get_opcode(instruction)
    instruction_type = get_instruction_type(opcode)
    decoded_instruction = {"type": instruction_type, "opcode": opcode}

    if instruction_type == "R-Type":
        decoded_instruction.update({"rs1": get_rs1(instruction),
                                    "rs2": get_rs2(instruction),
                                    "rd": get_rd(instruction),
                                    "func3": get_func3(instruction),
                                    "func7": get_func7(instruction)})
    elif instruction_type == "I-Type":
        decoded_instruction.update({"rs1": get_rs1(instruction),
                                    "rd": get_rd(instruction),
                                    "immediate": get_immediate(instruction, instruction_type)})
    elif instruction_type == "S-Type" or instruction_type == "B-Type":
        decoded_instruction.update({"rs1": get_rs1(instruction),
                                    "rs2": get_rs2(instruction),
                                    "func3": get_func3(instruction),
                                    "immediate": get_immediate(instruction, instruction_type)})
    # U-Type or J-Type
    else:
        decoded_instruction.update({"rd": get_rd(instruction),
                                    "immediate": get_immediate(instruction, instruction_type)})

    return decoded_instruction