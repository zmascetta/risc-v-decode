from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, header as header, convert as convert

'''
I-Instruction
Handles the signed/unsigned NON-SHIFT i-instructions.
Components: Opcode, Func3, RS1, RD, Immediate (12-digit, signed/unsigned)
Unsigned instructions: sltiu, sltu, lbu, lhu
'''
def regular_instruction(instruction, opcode, func3):
    lookup_value = opcode + func3
    spacing_list = (12, 5, 3, 5, 7)
    spacing_label = "imm--------| rs1-| f3| rd--| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "i-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "I-Type",
                    "source": header_info["source"],
                    "opcode": opcode,
                    "func3": func3}

    # Create rs1 dict.
    rs1_info = convert.register_conversion(decode.get_rs1(instruction))

    # Create rd dict.
    rd_info = convert.register_conversion(decode.get_rd(instruction))

    # Create imm. dict.
    immediate = instruction[0:12]
    imm_info = {"binary_value": immediate}
    if header_info["short_name"] in ("sltiu", "sltu", "lbu", "lhu"):
        imm_info.update(convert.unsigned_conversion(immediate))
    else:
        imm_info.update(convert.signed_conversion(immediate))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rd=rd_info["alias"], rs1=rs1_info["alias"], imm=imm_info["decimal_value"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                            "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rd_info": rd_info,
                           "imm_info": imm_info,
                           "assembly_info": assembly_text}

    return decoded_instruction

'''
I-Instruction (Shift):
Separate i-instruction function to handle the shift immediate instructions.
Components: Opcode, Func3, Func7, RS1, RD, SHAMT (5-digit)
'''
def shift_instruction(instruction, opcode, func3):
    func7 = decode.get_func7(instruction)
    lookup_value = opcode + func3 + func7
    spacing_list = (7, 5, 5, 3, 5, 7)
    spacing_label = "f7----|shamt| rs1-| f3| rd--| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "i-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "I-Type (shift)",
                    "source": header_info["source"],
                    "opcode": opcode,
                    "func3": func3,
                    "func7": func7}

    # Create rs1 dict.
    rs1_info = convert.register_conversion(decode.get_rs1(instruction))

    # Create rd dict.
    rd_info = convert.register_conversion(decode.get_rd(instruction))

    # Create shamt dict.
    # SHAMT[5] always equals 0
    shamt = instruction[7:12]
    if shamt[0] == 1:
        error_message = "Invalid shift amount. Your instruction is not valid."
        errorcheck.system_exit(error_message)

    shamt_info = {"binary_value": shamt}
    shamt_info.update(convert.unsigned_conversion(shamt))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rd=rd_info["alias"], rs1=rs1_info["alias"], shamt=shamt_info["decimal_value"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                            "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rd_info": rd_info,
                           "shamt_info": shamt_info,
                           "assembly_info": assembly_text}

    return decoded_instruction


def decode_instruction(instruction, opcode):
    func3 = decode.get_func3(instruction)
    shift_instruction_list = ("001", "101")

    if opcode == "0010011" and func3 in shift_instruction_list:
        decoded_instruction = shift_instruction(instruction, opcode, func3)
    else:
        decoded_instruction = regular_instruction(instruction, opcode, func3)

    return decoded_instruction