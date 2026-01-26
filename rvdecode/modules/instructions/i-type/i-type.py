from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck

'''
I-Instruction
Handles the signed/unsigned NON-SHIFT i-instructions.
Components: Opcode, Func3, RS1, RD, Immediate (12-digit, signed/unsigned)
Unsigned instructions: sltiu, sltu, lbu, lhu
'''
def i_instruction(instruction, opcode, func3):

    # Create header dict.
    header_info = create_header_info(instruction,"i_type")

    instruction_lookup_value = opcode + func3
    instruction_lookup = {
                "1100111000": {"short_name":  "jalr", "full_name": "jump and link register"},
                "0000011000": {"short_name":  "lb", "full_name": "load byte"},
                "0000011001": {"short_name":  "lh", "full_name": "load halfword"},
                "0000011010": {"short_name":  "lw", "full_name": "load word"},
                "0000011100": {"short_name":  "lbu", "full_name": "load byte, unsigned"},
                "0000011101": {"short_name":  "lhu", "full_name": "load halfword, unsigned"},
                "0010011000": {"short_name":  "addi", "full_name": "add immediate"},
                "0010011010": {"short_name":  "slti", "full_name": "set if less than immediate"},
                "0010011011": {"short_name":  "sltiu", "full_name": "set if less than immediate, unsigned"},
                "0010011100": {"short_name":  "xori", "full_name": "exclusive-OR immediate"},
                "0010011110": {"short_name":  "ori", "full_name": "OR immediate"},
                "0010011111": {"short_name":  "andi", "full_name": "AND immediate"}}
    try:
        instruction_lookup[instruction_lookup_value]
    except KeyError:
        error_message = "Invalid func3. Your instruction is not valid."
        errorcheck.system_exit(error_message)
    else:
        header_info.update(instruction_lookup[instruction_lookup_value])

    # Create general info dict.
    general_info = {"instruction_type": "I-Type",
                    "instruction_set": INSTRUCTION_SET,
                    "opcode": opcode,
                    "func3": func3}

    # Create rs1 dict.
    rs1_info = decode.register_conversion(decode.get_rs1(instruction))

    # Create rd dict.
    rd_info = decode.register_conversion(decode.get_rd(instruction))

    # Create imm. dict.
    immediate = instruction[0:12]
    imm_info = {"binary_value": immediate}
    if header_info["short_name"] in ("sltiu", "sltu", "lbu", "lhu"):
        imm_info.update(decode.unsigned_immediate_conversion(immediate))
    else:
        imm_info.update(decode.signed_immediate_conversion(immediate))

    # Create assembly info dict
    assembly_info = {"name": header_info["short_name"],
                     "rd": rd_info["alias"],
                     "rs1": rs1_info["alias"],
                     "imm": imm_info["decimal_value"]}

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rd_info": rd_info,
                           "imm_info": imm_info,
                           "assembly_info": assembly_info}

    return decoded_instruction



'''
I-Instruction (Shift):
Separate i-instruction function to handle the shift immediate instructions.
Components: Opcode, Func3, Func7, RS1, RD, SHAMT (6-digit)
'''
def i_instruction_shift(instruction, opcode, func3):

    # Create header dict.
    header_info = create_header_info(instruction, "i_instruction")

    # func3 + func7 is lookup value
    func7 = decode.get_func7(instruction)
    instruction_lookup = {
                "0010000000": {"short_name": "slli", "full_name": "shift left logical immediate"},
                "1010000000": {"short_name": "srli", "full_name": "shift right logical immediate"},
                "1010100000": {"short_name": "srai", "full_name": "shift right arithmetic immediate"}}
    header_info.update(decode.instruction_lookup(func3+func7, instruction_lookup, "Invalid func3 and/or func7."))

    # Create general info dict.
    general_info = decode.create_general_info("I-Type (Shift)", INSTRUCTION_SET, opcode, func3=func3, func7=func7)

    # Create rs1 dict.
    rs1_info = decode.register_conversion(decode.get_rs1(instruction))

    # Create rd dict.
    rd_info = decode.register_conversion(decode.get_rd(instruction))

    # Create shamt dict.
    # SHAMT[5] always equals 0
    shamt = instruction[8:15]
    if shamt[0] == 1:
        error_message = "Invalid shift amount. Your instruction is not valid."
        errorcheck.system_exit(error_message)

    shamt_info = {"binary_value": shamt}
    shamt_info.update(decode.unsigned_immediate_conversion(shamt))

    # Create assembly info dict
    assembly_info = {"name": header_info["short_name"],
                     "rd": rd_info["alias"],
                     "rs1": rs1_info["alias"],
                     "imm": shamt_info["decimal_value"]}

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rd_info": rd_info,
                           "shamt_info": shamt_info,
                           "assembly_info": assembly_info}

    return decoded_instruction