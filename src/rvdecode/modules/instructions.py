from . import header, decode, convert
import typer

'''
R-Instruction
 Components: Opcode, Func3, Func7, RS1, RS2, RD
'''
def decode_r_type(instruction, opcode):
    func3 = decode.get_func3(instruction)
    func7 = decode.get_func7(instruction)
    lookup_value = opcode+func3+func7
    spacing_list = (7, 5, 5, 3, 5, 7)
    spacing_label = "f7----| rs2-| rs1-| f3| rd--| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "r-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "R-Type",
                    "source": header_info["source"],
                    "opcode": opcode,
                    "func3": func3,
                    "func7": func7}

    # Create rs1 dict.
    rs1_info = convert.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = convert.register_conversion(decode.get_rs2(instruction))

    # Create rd dict.
    rd_info = convert.register_conversion(decode.get_rd(instruction))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rd=rd_info["alias"], rs1=rs1_info["alias"], rs2=rs2_info["alias"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                            "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "rd_info": rd_info,
                           "assembly_info": assembly_text}

    return decoded_instruction


'''
Decode I-Instruction
Decides whether instruction is regular or shift i-type
'''
def decode_i_type(instruction, opcode, rv64):
    func3 = decode.get_func3(instruction)
    shift_instruction_list_opcode = ("0010011", "0011011")
    shift_instruction_list_func3 = ("001", "101")

    if opcode in shift_instruction_list_opcode and func3 in shift_instruction_list_func3:
        decoded_instruction = decode_shift_i_type(instruction, opcode, func3, rv64)
    else:
        decoded_instruction = decode_regular_i_type(instruction, opcode, func3)

    return decoded_instruction

'''
I-Instruction
Handles the signed/unsigned NON-SHIFT i-instructions.
Components: Opcode, Func3, RS1, RD, Immediate (12-digit, signed/unsigned)
Unsigned instructions: sltiu, sltu, lbu, lhu
'''
def decode_regular_i_type(instruction, opcode, func3):
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
    imm_info = {"binary": immediate}
    if header_info["short_name"] in ("sltiu", "sltu", "lbu", "lhu"):
        imm_info.update(convert.unsigned_conversion(immediate))
    else:
        imm_info.update(convert.signed_conversion(immediate))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rd=rd_info["alias"], rs1=rs1_info["alias"], imm=imm_info["decimal"])

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
def decode_shift_i_type(instruction, opcode, func3, rv64):
    if rv64:
        func7 = instruction[0:6]
        spacing_list = (6, 6, 5, 3, 5, 7)
        spacing_label = "f7---| shamt| rs1-| f3| rd--| opcode|\n"
    else:
        if instruction[6] == "1":
            print("You entered a shift instruction without indicating RV64 and the instruction is invalid in RV32I. Please run your command again using the \"--rv64\" option")
            raise typer.Exit(code=1)
        func7 = decode.get_func7(instruction)
        spacing_list = (7, 5, 5, 3, 5, 7)
        spacing_label = "f7----|shamt| rs1-| f3| rd--| opcode|\n"

    lookup_value = opcode + func3 + func7

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
    # SHAMT[5] always equals 0 in RV32
    if rv64:
        shamt = instruction[6:12]
    else:
        shamt = instruction[7:12]
        if shamt[0] == 1:
            print("Invalid shift amount. Your instruction is not valid.")
            raise typer.Exit(code=1)

    shamt_info = {"binary": shamt}
    shamt_info.update(convert.unsigned_conversion(shamt))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rd=rd_info["alias"], rs1=rs1_info["alias"], shamt=shamt_info["decimal"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rd_info": rd_info,
                           "shamt_info": shamt_info,
                           "assembly_info": assembly_text}

    shift_list = ("slli", "srli", "srai")
    if header_info["short_name"] in shift_list and not rv64:
        print("NOTE: You entered a shift command without indicating its origin. By default, the RV32I result is displayed below. If your instruction came from RV64I, please rerun with the \"--rv64\" option\n")
    return decoded_instruction



'''
S-Instruction:
Components: Opcode, Func3, RS1, RS2, Offset
'''
def decode_s_type(instruction, opcode):
    func3 = decode.get_func3(instruction)
    lookup_value = opcode+func3
    spacing_list = (7, 5, 5, 3, 5, 7)
    spacing_label = "off---| rs2-| rs1-| f3| off-| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "s-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "S-Type",
                    "source": header_info["source"],
                    "opcode": opcode,
                    "func3": func3}

    # Create rs1 dict.
    rs1_info = convert.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = convert.register_conversion(decode.get_rs2(instruction))

    # Create offset dict
    offset = instruction[0:8] + instruction[20:25]
    off_info = {"binary": offset}
    off_info.update(convert.signed_conversion(offset))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rs1=rs1_info["alias"], rs2=rs2_info["alias"], imm=off_info["decimal"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "off_info": off_info,
                           "assembly_info": assembly_text}

    return decoded_instruction


'''
B-Instruction
 Components: Opcode, Func3, Func7, RS1, RS2, Imm
'''
def decode_b_type(instruction, opcode):
    func3 = decode.get_func3(instruction)
    lookup_value = opcode+func3
    spacing_list = (7, 5, 5, 3, 5, 7)
    spacing_label = "off---| rs2-| rs1-| f3| off-| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "b-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "B-Type",
                    "source": header_info["source"],
                    "opcode": opcode,
                    "func3": func3}

    # Create rs1 dict.
    rs1_info = convert.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = convert.register_conversion(decode.get_rs2(instruction))

    # Create offset dicts.

    off_instr_info = {"binary": instruction[0:8] + " " + instruction[20:24]}

    final_value = instruction[0:1] + instruction[24:25] + instruction[1:7] + instruction[20:24] + "0"
    off_final_info = {"binary": final_value}

    # check if signed or unsigned for correct conversion
    unsigned_list = ("bltu", "bgeu")
    if header_info["short_name"] in unsigned_list:
        off_final_info.update(convert.unsigned_conversion(final_value))
    else:
        off_final_info.update(convert.signed_conversion(final_value))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rs1=rs1_info["alias"], rs2=rs2_info["alias"], imm=off_final_info["decimal"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "off_instr_info": off_instr_info,
                           "off_final_info": off_final_info,
                           "assembly_info": assembly_text}

    return decoded_instruction


'''
U-Instruction:
Components: Opcode, RD, Immediate
'''
def decode_u_type(instruction, opcode):
    lookup_value = opcode
    spacing_list = (20, 5, 7)
    spacing_label = "imm----------------| rd--| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "u-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "U-Type",
                    "source": header_info["source"],
                    "opcode": opcode}

    # Create rd dict.
    rd_info = convert.register_conversion(decode.get_rd(instruction))

    # Create immediate dicts.
    immediate = instruction[0:20]
    u_imm_instr_info = {"binary": immediate}
    u_imm_instr_info.update(convert.unsigned_conversion(immediate))

    immediate = immediate.ljust(32,"0")
    u_imm_final_info = {"binary": immediate}
    u_imm_final_info.update(convert.unsigned_conversion(immediate))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], imm=u_imm_instr_info["hex"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rd_info": rd_info,
                           "u_imm_instr_info": u_imm_instr_info,
                           "u_imm_final_info": u_imm_final_info,
                           "assembly_info": assembly_text}

    return decoded_instruction


'''
J-Instruction:
Components: Opcode, RD, Immediate
'''
def decode_j_type(instruction, opcode):
    lookup_value = opcode
    spacing_list = (20, 5, 7)
    spacing_label = "imm----------------| rd--| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "j-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "J-Type",
                    "source": header_info["source"],
                    "opcode": opcode}

    # Create rd dict.
    rd_info = convert.register_conversion(decode.get_rd(instruction))

    # Create immediate dicts.
    immediate = instruction[0:20]
    off_instr_info = {"binary": immediate}

    immediate = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + "0"
    off_final_info = {"binary": immediate}
    off_final_info.update(convert.unsigned_conversion(immediate))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rd=rd_info["alias"], imm=off_final_info["hex"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rd_info": rd_info,
                           "off_instr_info": off_instr_info,
                           "off_final_info": off_final_info,
                           "assembly_info": assembly_text}

    return decoded_instruction