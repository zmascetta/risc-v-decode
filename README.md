
# 🔎 RISC-V Decode  
A CLI program for decoding RISC-V instructions.

## Features  
 - Displays information for all registers used by instruction, including name, alias and use.
 - Displays immediate/offset values in binary, decimal, and hex.
 - Displays both "value in instruction" and final value for instructions whose immediate/offset require transformation(s) (repositioning bits, zero extending, etc.).
 - Outputs assembly code (with obvious limitations due to decompilation)
 - Displays formatted instruction with labels for each component
 - Support for RV32I, RV64I, RV32M, and RV64M instructions (minus fence, ecall, ebreak, and CSR instructions)
  
## Background
This is a tool I built while learning RISC-V Assembly Language to better understand the ISA and how instructions are created/formatted. There probably isn't too much practical, day-to-day use for this, but it proved a good learning aid. There were times when I wanted to check my work (especially when manually writing full binary instructions) or check how my code had compiled. This made it easier than having to manually extract the information from the instruction.

It was created using Typer and has the necessary components to build using `uv`.

## Usage  

     rvdecode [INSTRUCTION]

 - Instruction can be binary or hex. It can also contain spaces if it is enclosed by quotes.
  
## Example Output

    Any of the inputs below will produce the following output:
    rvdecode "0000 0000 0101 1110 0000 1110 0011 0011"
    rvdeocde 00000000010111100000111000110011
    rvdecode 0x5e0e33
    rvdecode 5e0e33

    Add (add)
    00000000010111100000111000110011
    0x5e0e33
    
    f7----| rs2-| rs1-| f3| rd--| opcode|
    0000000 00101 11100 000 11100 0110011
    
    General Information
    Instruction Type: R-Type
    Source: RV32I/RV64I
    Opcode: 0110011
    Func3: 000
    Func7: 0000000
    
    Source Register 1 (rs1)
    Binary Value: 11100
    Decimal Value: 28
    Name: x28
    Alias: t3
    Use: temporary
    
    Source Register 2 (rs2)
    Binary Value: 00101
    Decimal Value: 5
    Name: x5
    Alias: t0
    Use: temporary
    
    Destination Register (rd)
    Binary Value: 11100
    Decimal Value: 28
    Name: x28
    Alias: t3
    Use: temporary
    
    Assembly Code
    add t3, t3, t0