import sys, importlib, typer
from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, output as output

app = typer.Typer()


def main(instruction: str):

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
    typer.run(main)

