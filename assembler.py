"""
Some Terminology:
1. rs: Source register.
2. rd: Destination register.
3. rt: Temporary register.
4. imm: Immediate.
5. PC: Program Counter.
6. sp: Stack Pointer.
"""

import R_encoding
from registers import Register,register_address

# Initializing Registers with values set to 0

registers={}

for i in range(32):
    key = "r"+str(i)
    registers[key]=Register(register_address[key])

# Reading Assembly

out=[]

assembly = open("test_assembly.txt","r")

instructions=assembly.readlines()

# Assuming Instructions are of the form "operation r1,r2,r3"

for instruction in instructions:
    instruction=instruction.strip() # Removing /n from each line
    # but what about last line you ask -> we shall worry about it later
    
    inp=instruction.split(" ")
    operation = inp[0]

    # R-Type Instruction
    if operation in R_encoding.R_operations:
        final=""
        final+=R_encoding.R_opcode
        #We will also worry about performing the actual operation later

        rd,rs1,rs2=inp[1].split(",") # gives us rd,rs1,rs2 IN THAT ORDER

        final+=register_address[rd]
        final+=R_encoding.R_funct3[operation]
        final+=register_address[rs1]
        final+=register_address[rs2]
        final+=R_encoding.R_funct7[operation]

        out.append(final)

assembly.close()

# Outputting to a txt file for now....

output = open("test_out.txt","w")

for x in out:
    output.write(x+"\n")

output.close()