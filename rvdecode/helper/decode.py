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
        immediate = instruction[0:12]
    elif instruction_type == "S-Type":
        immediate = instruction[0:8] + instruction[20:25]
    elif instruction_type == "B-Type":
        immediate = instruction[0:0] + instruction[24:25] + instruction[1:7] + instruction[20:24] + "0"
    elif instruction_type == "U-Type":
        immediate = instruction[0:20].ljust(32,"0")
    else:   #J-Type
        immediate = instruction[0:1] + instruction[12:20] + instruction[11:12] + instruction[1:11] + "0"
        immediate.zfill(32)

    imm_width = len(immediate)
    return (immediate, imm_width)


# identify instruction type via opcode
def get_instruction_type(opcode):
    instruction_reference = {"1101111": "J-type",
                             "1100011": "B-Type",
                             "0110011": "R-Type",
                             "0100011": "S-Type",
                             "0110111": "U-Type",
                             "0010111": "U-Type",
                             "0000011": "I-Type",
                             "0010011": "I-Type",
                             "0001111": "I-Type",
                             "1110011": "I-Type"}

    # exit if invalid opcode
    if opcode not in instruction_reference:
        extra_lines = "ERROR: Opcode in instruction is not valid."
        errorcheck.system_exit(extra_lines)

    return instruction_reference[opcode]


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
        return decoded_instruction

    # get imm. value and width
    immediate = get_immediate(instruction, instruction_type)

    if instruction_type == "I-Type":
        decoded_instruction.update({"rs1": get_rs1(instruction),
                                    "rd": get_rd(instruction),
                                    "immediate": immediate[0],
                                    "imm_width": immediate[1]})
    elif instruction_type == "B-Type":
        decoded_instruction.update({"rs1": get_rs1(instruction),
                                    "rs2": get_rs2(instruction),
                                    "func3": get_func3(instruction),
                                    "immediate": immediate[0],
                                    "imm_width": immediate[1]})
    elif instruction_type == "S-Type":
        func3 = get_func3(instruction)

        # slli, srli, srai have s-type opcode but instruction resembles r-type.
        if func3 in ("001", "101"):
            decoded_instruction.update({"rs1": get_rs1(instruction),
                                        "shamt": get_rs2(instruction), # rs2 field is effectively the shift amount for imm. versions of shift instr.
                                        "rd": get_rd(instruction),
                                        "func3": func3,
                                        "func7": get_func7(instruction)})
        else:
            decoded_instruction.update({"rs1": get_rs1(instruction),
                                        "rs2": get_rs2(instruction),
                                        "func3": func3,
                                        "immediate": immediate[0],
                                        "imm_width": immediate[1]})
    # U-Type or J-Type
    else:
        decoded_instruction.update({"rd": get_rd(instruction),
                                    "immediate": immediate[0],
                                    "imm_width": immediate[1]})
    return decoded_instruction