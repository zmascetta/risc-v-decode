
# 🔎 RISC-V Decode  
A CLI program for decoding RISC-V instructions.

## Current Features  
 - Displays information for all registers used by instruction, including name, alias and use.
 - Displays immediate/offset values in binary, decimal, and hex.
 - Displays both "value in instruction" and final value for instructions whose immediate/offset require transformation(s) (repositioning bits, zero extending, etc.).
 - Outputs assembly code
 - Displays formatted instruction with labels for each component
 - Support for RV32I instructions  (support for additional base-ISA's and extensions coming soon)
  
## Usage  

     rvdecode [INSTRUCTION]

 - Instruction can be binary or hex. It can also contain spaces if it is enclosed by quotes.
  
## Example Output

    rvdecode "0000 0000 0101 1110 0000 1110 0011 0011"

    Add (add)
    00000000010111100000111000110011
    
    f7----| rs2-| rs1-| f3| rd--| opcode|
    0000000 00101 11100 000 11100 0110011
    
    General Information
    Instruction Type: R-Type
    Source: RV32I
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




