import typer

# opcode
def get_opcode(instruction):
    return instruction[-7:]

# identify instruction type via opcode
def get_instruction_type(opcode):
    instruction_list = {"1101111": "j-type",
                        "1100011": "b-type",
                        "0110011": "r-type",
                        "0111011": "r-type",
                        "0100011": "s-type",
                        "0110111": "u-type",
                        "0010111": "u-type",
                        "0000011": "i-type",
                        "0010011": "i-type",
                        "1100111": "i-type",
                        "0011011": "i-type"}

    try:
        instruction_type = instruction_list[opcode]
    except KeyError:
        print("ERROR: Instruction opcode is not valid.")
        raise typer.Exit(code=1)
    else:
        return instruction_type


# registers
def get_rs1(instruction):
    return instruction[12:17]

def get_rs2(instruction):
    return instruction[7:12]

def get_rd(instruction):
    rd = instruction[20:25]

    if rd == "00000":
        if instruction[-7:] == "1100111":
            return rd
        else:
            print("ERROR: Attempt to write to x0.")
            raise typer.Exit(code=1)

    return rd


# funcs
def get_func3(instruction):
    return instruction[17:20]

def get_func7(instruction):
    return instruction[0:7]


# Make assembly code text
def make_assembly_code(name, rd=None, rs1=None, rs2=None, shamt=None, imm=None):
    assembly_components = locals()

    assembly_list = []
    for key, val in assembly_components.items():
        if val is not None:
            if key in ("rs1", "rs2") and val == "zero":
                assembly_list.append("x0")
            else:
                assembly_list.append(str(val))

    # add formatting
    # do not add a comma if component is the first or the last component
    length = len(assembly_list)
    x = 0
    assembly_text = ""
    while x < length:
        if x > 0 and x < length - 1:
            assembly_text += assembly_list[x] + ", "
        else:
            assembly_text += assembly_list[x] + " "
        x += 1

    return assembly_text