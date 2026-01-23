import sys
from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, output as output


def main():

    # assign instruction
    instruction = sys.argv[1].replace(" ","")

    # perform error checks
    errorcheck.argument_check(sys.argv)
    errorcheck.instruction_check(instruction)

    # perform instruction decode
    opcode, instruction_set = decode.get_opcode(instruction)


    # print output
    output.output_instruction(decoded_instruction)


if __name__ == "__main__":
    main()

