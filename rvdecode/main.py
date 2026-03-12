import sys, importlib
from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, output as output


def main():

    # strip whitespace
    instruction = sys.argv[1].replace(" ","")

    # perform error checks
    errorcheck.argument_check(sys.argv)
    # check if help flagged used
    if sys.argv[1] in ("-h","--help"):
        output.print_help()
    # check if valid bin/hex instruction entered
    instruction = errorcheck.instruction_check(instruction)

    # get opcode and instruction type.
    opcode = decode.get_opcode(instruction)
    instruction_type = decode.get_instruction_type(opcode)

    # import corresponding module
    instruction_module = importlib.import_module(f"modules.instructions.{instruction_type}.{instruction_type}")

    # decode instruction
    decoded_instruction = instruction_module.decode_instruction(instruction, opcode)

    # print output
    output.output_instruction(decoded_instruction)

    exit(0)


if __name__ == "__main__":
    main()

