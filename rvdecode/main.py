import sys
from rvdecode.modules import decode as decode, errorcheck as errorcheck, output as output


def main():

    # assign instruction
    instruction = sys.argv[1].replace(" ","")

    # perform error checks
    errorcheck.argument_check(sys.argv)
    errorcheck.instruction_check(instruction)

    # perform instruction decode
    decoded_instruction = decode.decode_instruction(instruction)

    # print output
    output.output_instruction(decoded_instruction)


if __name__ == "__main__":
    main()

