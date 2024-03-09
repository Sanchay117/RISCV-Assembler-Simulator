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

def binary_to_specified_len(num,length):

    # I)Converts a number to unsigned binary string representation with as minimum bits as possible eg: 5 to 0b101
    # II)Converts The binary string "0bxyz" to specified length by adding required bits.(Sign Extension) eg: if length = 5, 5 to 0b101 to "00101"
            
    # Note: for negative numbers -> Their  binary representation are acheived by taking 2's complement of binary representation of abs(num) 
    #                            -> To do this we perform bitwise xor operation between A(binary representation of abs(num)) 
    #                               and B(binary of max reprensentable value using "length" amount of bits{111...length times}) and then add 1 to result.
    #                            -> In python if we perform 10^5 ("^" sign for xor)then,by default bitwise xor is performed on binary 
    #                               representation of 10 and 5 i.e.(1010 and 0101)
                                 
    # For example:1) num = 3
    #              the built in func (bin) : bin(3) returns "0b11"
    #              if length  = 5 we get string as "00011"

    #             2) num  = -10, length = 5
    #              bin(10) = 1010
    #              The expression[bin((abs(num)^((2**length)-1)) + 1)] = [bin(10^31)+1] = bin({01010^11111 in binary} +1) = "10110" 
    


    if(num>=0):
        bin_string = bin(num)   
        bin_string = bin_string[2:]
        bin_string = '0'*(length-len(bin_string)) + bin_string  #extended by adding 0 to leftmost side

    elif(num<0):
        bin_string = bin((abs(num)^((2**length)-1)) + 1)    # bitwise xor between a(abs(num)) and b(decimal value of binary number 1111....length times) followed by addition of 1
        bin_string = bin_string[2:]                        
        bin_string = '1'*(length-len(bin_string)) + bin_string    # extended by adding 1 to leftmost side
 
    return bin_string


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

        out.append(final)

    # I-Type Instruction
    elif operation in I_encoding.I_operations:
        final = I_encoding.I_oppcode[operation]
        if operation == "lw":
            rd, other = inp[1].split(",")
            tempimm, rs = other.split("(")
            rs = rs.rstrip(")")
            final = binary_to_specified_len(int(tempimm), 12) + register_address[rs] + I_encoding.I_funct3[operation] + register_address[rd] + final
        else:
            rd, rs, other = inp[1].split(",") #gives us rd, rs1 and imm/offset
            final = binary_to_specified_len(int(other), 12) + register_address[rs] + I_encoding.I_funct3[operation] + register_address[rd] + final
        out.append(final)
    
    #J-Type Instruction
    elif operation in J_encoding.J_operations:
        rd, tempimm = inp[1].split(",")
        final = binary_to_specified_len(int(tempimm), 20) + register_address[rd] + J_encoding.J_oppcode
        out.append(final)
    
    # Branching
    
    elif operation in B_encoding.B_operations:
        
        rs1,rs2,imm=inp[1].split(",")
        branch=int(imm)
        branch-=1
        # binary=bin(int(imm))
        imm_12bit = binary_to_specified_len(int(imm),12)
        final = imm_12bit[-12:-5] + register_address[rs2] + register_address[rs1] + B_encoding.B_funct3[operation] + imm_12bit[-5:] + B_encoding.B_oppcode

        val1,val2=registers[rs1].value,registers[rs2].value

        if(operation=="beq"):
            if(val1==val2) :
                pc+=branch

        elif(operation=="bne"):
            if(val1!=val2):
                pc+=branch

        elif(operation=="bge"):
            # Remember to use signed comparison later
            if(val1>=val2):
                pc+=branch

        elif(operation=="bgeu"):
            # Remember to use unsigned comparison later
            if(val1>=val2):
                pc+=branch

        elif(operation=="blt"):
            # Remember to use signed comparison later
            if(val1<val2):
                pc+=branch
        
        else:
            # Remember to use unsigned comparison later
            if(val1<val2):
                pc+=branch

        out.append(final)

    # S-Type Instruction
    elif operation in S_encoding.S_operations:
        
        rs2,k = inp[1].split(',')    #splitting to get for example: rs2,k =  t1,20(t0)
        k = k.rstrip(')')               # k = 20(t0
        imm,rs1 = k.split('(')      #imm,rs1 = 20,t0

        imm = binary_to_specified_len(int(imm),12)      #converting immediate value to 12bit binary string

        final = imm[-12:-5] + register_address[rs2] + register_address[rs1] + S_encoding.S_funct3[operation] + imm[-5:] + S_encoding.S_oppcode

        out.append(final)

    # U-Type Instruction
    elif operation in U_encoding.U_operations:

        rd,imm = inp[1].split(',')      #splitting to get for example rd,imm = t0,20

        imm = binary_to_specified_len(int(imm),32) #converting immediate value to 32 bits binary string

        final = imm[-32:-12] + register_address[rd] + U_encoding.U_oppcode[operation]

        out.append(final)

    pc+=1 # Always keep this at the last of the loop!!!
    

assembly.close()

# Outputting to a txt file for now....

output = open("test_out.txt","w")

for x in out:
    output.write(x+"\n")

output.close()
