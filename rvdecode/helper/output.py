'''
specific type - use func, store specific, add, addi, etc.

immediate decode - store, convert to hex and dec
registers decode - store, convert to ABI
make assembly line

0000000 00001 00000 000 00101 0010011
00000000000100000000001010010011
'''

def lookup_instruction(opcode, func3=None, func7=None):
    pass


def immediate_conversion(immediate):
    immediate_data = {"value": immediate,
                        "bin": "0b" + str(int(immediate, base=2)),
                        "dec": str(int(immediate)),
                        "hex": "0x"+ str(int(immediate, base=16))}
    return immediate_data


def register_conversion(register_value):
    register_data = {"value": register_value,
                     "name": "asdf",
                     "alias": "asdf",
                     "use": "asdf"
                     }
    pass


def print_output(decoded_instruction):
    pass

imm = immediate_conversion("000000000001")
print(imm)