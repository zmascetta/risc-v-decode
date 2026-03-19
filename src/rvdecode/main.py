import typer
from typing import Annotated
from .modules import decode, errorcheck, instructions, output

app = typer.Typer()


@app.command()
def main(instruction: Annotated[str, typer.Argument(help="A valid 32-bit binary or 6-bit hex instruction.")],
         rv64: Annotated[
             bool,
             typer.Option(
                 help="Only used with slli, srli, or srai instruction."
             ),
         ] = False,
         ):
    # check if valid bin/hex instruction entered
    instruction = errorcheck.instruction_check(instruction)

    # get opcode and instruction type.
    opcode = decode.get_opcode(instruction)
    instruction_type = decode.get_instruction_type(opcode)

    # decode instruction
    if instruction_type == "r-type":
        decoded_instruction = instructions.decode_r_type(instruction, opcode)
    elif instruction_type == "i-type":
        decoded_instruction = instructions.decode_i_type(instruction, opcode, rv64)
    elif instruction_type == "s-type":
        decoded_instruction = instructions.decode_s_type(instruction, opcode)
    elif instruction_type == "b-type":
        decoded_instruction = instructions.decode_b_type(instruction, opcode)
    elif instruction_type == "u-type":
        decoded_instruction = instructions.decode_u_type(instruction, opcode)
    else:
        decoded_instruction = instructions.decode_j_type(instruction, opcode)

    # print output
    output.output_instruction(decoded_instruction)