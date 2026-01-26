import sys, importlib
from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, output as output


def main():

    # strip whitespace
    instruction = sys.argv[1].replace(" ","")

    # perform error checks
    errorcheck.argument_check(sys.argv)
    errorcheck.instruction_check(instruction)

    # get opcode and source ISA/extension.
    opcode = decode.get_opcode(instruction)
    source = decode.get_source(opcode)

    # import corresponding module
    instruction_module = importlib.import_module(f"rvdecode.modules.instructions.{source}.{source}")







    # print output
    output.output_instruction(decoded_instruction)


if __name__ == "__main__":
    main()

