"""
Some Terminology:
1. rs: Source register.
2. rd: Destination register.
3. rt: Temporary register.
4. imm: Immediate.
5. PC: Program Counter.
6. sp: Stack Pointer.
"""

import Encoding.R_encoding as R_encoding
import Encoding.I_encoding as I_encoding
import Encoding.S_encoding as S_encoding
import Encoding.B_encoding as B_encoding
import Encoding.U_encoding as U_encoding
import Encoding.J_encoding as J_encoding

from registers import Register,register_address

# Functions

def binary_to_specified_len(binary,length):

    # Converts The binary string "0bxyz" to specified length
    # For example the built in func (bin) : bin(3) returns "0b11"
    # so if this function is called with ("0b11",5) it will return : "00011" (with 5 binary digits)

    binary=binary[2:]
    trailing_zeros=length-len(binary)
    return ("0"*trailing_zeros + binary)

# Initializing Registers with values set to 0

registers={}

for key in register_address:
    registers[key]=Register(register_address[key])

# Reading Assembly

out=[]

assembly = open("test_assembly.txt","r")

instructions=assembly.readlines()

# Assuming Instructions are of the form "operation r1,r2,r3"
# That is operation and operands seperated by space and operands themselves seperated by commas

lines=len(instructions)

pc=0 # program counter

while pc<lines:

    instruction = instructions[pc]

    instruction=instruction.strip() # Removing /n and spaces(leading and trailing both) from each line
    # but what about last line you ask -> we shall worry about it later
    
    inp=instruction.split(" ")
    operation = inp[0]

    # R-Type Instruction
    if operation in R_encoding.R_operations:

        #We will also worry about performing the actual operation later

        rd,rs1,rs2=inp[1].split(",") # gives us rd,rs1,rs2 IN THAT ORDER

        final = R_encoding.R_funct7[operation] + register_address[rs2] + register_address[rs1] + R_encoding.R_funct3[operation] + register_address[rd] +R_encoding.R_oppcode

    
    # Branching
    
    if operation in B_encoding.B_operations:
        
        rs1,rs2,imm=inp[1].split(",")
        binary=bin(int(imm))
        imm_12bit = binary_to_specified_len(binary,12)
        final = imm_12bit[-12:-5] + register_address[rs2] + register_address[rs1] + B_encoding.B_funct3[operation] + imm_12bit[-5:] + B_encoding.B_oppcode

    # S-Type Instruction
    if operation in S_encoding.S_operations:
        
        rs2,k = inp[1].split(',')    #splitting to get for example: rs2,k =  t1,20(t0)
        k = k.rstrip(')')               # k = 20(t0
        imm,rs1 = k.split('(')      #imm,rs1 = 20,t0

        imm = S_encoding.binary(imm)      #converting immediate value to 12bit binary string

        final = imm[-12:-5] + register_address[rs2] + register_address[rs1] + S_encoding.S_funct3[operation] + imm[-5:] + S_encoding.S_oppcode
    
    # U-Type Instruction
    if operation in U_encoding.U_operations:

        rd,imm = inp[1].split(',')      #splitting to get for example rd,imm = t0,20

        imm = U_encoding.binary(imm) #converting immediate value to 32 bits binary string

        final = imm[-32:-11] + register_address[rd] + U_encoding.U_oppcode

    out.append(final)

    pc+=1 # Always keep this at the last of the loop!!!
    

assembly.close()

# Outputting to a txt file for now....

output = open("test_out.txt","w")

for x in out:
    output.write(x+"\n")

output.close()