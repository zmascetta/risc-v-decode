import errorcheck

'''
instr. decode

overall type - use opcode store type r, i, s, b, u, j
specific type - use func, store specific, add, addi, etc.
immediate decode - store, convert to hex and dec
registers decode - store, convert to ABI
make assembly line


00000000000100000000001010010011
'''

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
        errorcheck.system_exit(extra_lines)

def instruction_decode(instruction):
    op_code = instruction[25:]
    instruction_type = get_instruction_type(op_code)

instruction_decode("00000000000100000000001010010011")
