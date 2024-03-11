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
import sys

input_file,output_file = sys.argv[1],sys.argv[2]

from registers import Register,register_address

# Functions

def binary_to_specified_len(num,length):

    # I)Converts a number to unsigned binary string representation with as minimum bits as possible eg: 5 to 0b101
    # II)Converts The binary string "0bxyz" to specified length by adding required bits.(Sign Extension) eg: if length = 5, 5 to 0b101 to "00101"
            
    # Note: for negative numbers -> Their  binary representation are acheived by taking 2's complement of binary representation of abs(num) 
    #                            -> To do this we perform bitwise xor operation between A(binary representation of abs(num)) 
    #                               and B(max representable value using "length" amount of bits {111...length times}) and then add 1 to result.
    #                            -> In python if we perform 10^5 ("^" sign for xor)then,by default bitwise xor is performed on binary 
    #                               representation of 10 and 5 i.e.(1010 and 0101) to give 1111.
                                 
    # For example:1)->num = 3 ,length = 5
    #               ->The built in func (bin) : bin(3) returns "0b11"
    #               ->If length  = 5 we get string as "00011"

    #             2)->num  = -10, length = 5
    #               ->bin(10) = 1010
    #               ->The expression[bin((abs(num)^((2**length)-1)) + 1)] = [bin(10^31)+1] = [(01010^11111) +1] = "0b10110" 
    


    if(num>=0):                                                 #eg:num = 5, length = 5
        bin_string = bin(num)                                   # Converting 5 to '0b101'
        bin_string = bin_string[2:]                             #Removing '0b'  to give '101'
        bin_string = '0'*(length-len(bin_string)) + bin_string  #extended by adding 0 to leftmost side to give '00101'

    elif(num<0):                                                #eg: num = -5 , length = 5
        bin_string = bin((abs(num)^((2**length)-1)) + 1)        #performing 2's complement bin(5^[2**5 - 1] + 1) -> bin(5^31 + 1) -> bin( )-> 11011
        bin_string = bin_string[2:]                             
        bin_string = '1'*(length-len(bin_string)) + bin_string  # extended by adding 1 to leftmost side
 
    return bin_string

# def signed_val(s):
#     # returns signed value of a binary string
#     if(s[0]==1):
#         return -1*int(s[1:],2)
#     else:
#         return int(s[1:],2)
    
# def unsigned_val(s):
#     return int(s,2)


# Initializing Registers with values set to 0

registers={}

for key in register_address:
    registers[key]=Register(register_address[key])

# Reading Assembly

out=[]

assembly = open(input_file,"r")
instructions=assembly.readlines()

#no of lines and check if last line is halt instruction or not 
no_of_lines = len(instructions) 
flag_halt_not_found = False if instructions[-1] != "beq zero,zero,0" else True 
# print(flag_halt_not_found)
# Assuming Instructions are of the form "operation r1,r2,r3"
# That is operation and operands seperated by space and operands themselves seperated by commas

lines=len(instructions)*4 # as Address starts at 0x00 and increment by 4. As, our processor is byte addressable and each instruction is of 32 bit.

# labels
labels={}

for line in range(int(lines/4)):
    instruction = instructions[line]
    instruction = instruction.strip().split(" ")
    if(instruction[0]!=""):
        if (instruction[0][-1]==":"):
            labels[instruction[0][:-1]] = line*4
            instructions[line]=" ".join(instruction[1:]) + "\n"


pc=0 # program counter

while pc<lines:

    instruction = instructions[int(pc/4)]

    instruction=instruction.strip() # Removing /n and spaces(leading and trailing both) from each line
    # but what about last line you ask -> we shall worry about it later
    
    inp=instruction.split(" ")
    operation = inp[0]

    # R-Type Instruction
    if operation in R_encoding.R_operations:

        #We will also worry about performing the actual operation later

        rd,rs1,rs2=inp[1].split(",") # gives us rd,rs1,rs2 IN THAT ORDER

        final = R_encoding.R_funct7[operation] + register_address[rs2] + register_address[rs1] + R_encoding.R_funct3[operation] + register_address[rd] +R_encoding.R_oppcode

        # val1,val2=registers[rs1].value,registers[rs2].value
        # signed_val1,signed_val2=signed_val(val1),signed_val(val2)
        # unsigned_val1,unsigned_val2=unsigned_val(val1),unsigned_val(val2)

        # if operation=="add":
        #     result = binary_to_specified_len(signed_val1+signed_val2,32)
        #     registers[rd].set(result)
        # elif operation=="sub":
        #     result = binary_to_specified_len(signed_val1-signed_val2,32)
        #     registers[rd].set(result)
        # elif operation=="slt":
        #     if(signed_val1<signed_val2):
        #         registers[rd].set(binary_to_specified_len(1,32))
        # elif operation=="sltu":
        #     if(unsigned_val1<unsigned_val2):
        #         registers[rd].set(binary_to_specified_len(1,32))
        # elif operation=="xor":
        #     result=""
        #     for i in range(len(val1)):
        #         if((val1[i]==1 or val2[i]==1) and not(val1==1 and val2==1)):
        #             result+="1"
        #         else:
        #             result+="0"
        #     registers[rd].set(result)
        # elif operation=="sll":
        #     shift=unsigned_val(val2[-5:])
        #     result=signed_val1<<shift
        #     registers[rd].set(binary_to_specified_len(result,32))
        # elif operation=="srl":
        #     shift=unsigned_val(val2[-5:])
        #     result=signed_val1>>shift
        #     registers[rd].set(binary_to_specified_len(result,32))
        # elif operation=="or":
        #     result=""
        #     for i in range(len(val1)):
        #         if((val1[i]==1 or val2[i]==1)):
        #             result+="1"
        #         else:
        #             result+="0"
        #     registers[rd].set(result)
        # else:
        #     result=""
        #     for i in range(len(val1)):
        #         if((val1[i]==1 and val2[i]==1)):
        #             result+="1"
        #         else:
        #             result+="0"
        #     registers[rd].set(result)
            

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
        imm = binary_to_specified_len(int(tempimm), 21)
        final =  imm[-21] + imm[-11:-1] + imm[-12] + imm[-20:-12]+ register_address[rd] + J_encoding.J_oppcode
        out.append(final)
    # Branching
    
    elif operation in B_encoding.B_operations:
        
        rs1,rs2,imm=inp[1].split(",")

        if(imm.isnumeric() or imm in labels):
            if (imm.isnumeric()):
                offset=int(imm)*4
                imm_13bit = binary_to_specified_len(int(imm),13)
            else:
                offset = labels[imm] - pc
                imm_13bit=binary_to_specified_len(offset,13)

            final = imm_13bit[-13] + imm_13bit[-11] + imm_13bit[-10:-5] + register_address[rs2] + register_address[rs1] + B_encoding.B_funct3[operation] + imm_13bit[-5:-1] + imm_13bit[-12] + B_encoding.B_oppcode
            # val1,val2=registers[rs1].value,registers[rs2].value

            # if(operation=="beq"):
            #     if(val1==val2) :
            #         pc+=offset

            # elif(operation=="bne"):
            #     if(val1!=val2):
            #         pc+=offset

            # elif(operation=="bge"):
            #     # Remember to use signed comparison later
            #     if(val1>=val2):
            #         pc+=offset

            # elif(operation=="bgeu"):
            #     # Remember to use unsigned comparison later
            #     if(val1>=val2):
            #         pc+=offset

            # elif(operation=="blt"):
            #     # Remember to use signed comparison later
            #     if(val1<val2):
            #         pc+=offset
            
            # else:
            #     # Remember to use unsigned comparison later
            #     if(val1<val2):
            #         pc+=offset
            
        else:
            if(imm not in labels):
                print("Error on line:",int(pc/4)+1,"->No such label")
                break

        out.append(final)

    # S-Type Instruction
    elif operation in S_encoding.S_operations:
        
        rs2,k = inp[1].split(',')    #splitting to get for example: rs2, k =  t1, 20(t0)
        k = k.rstrip(')')               # k = 20(t0
        imm,rs1 = k.split('(')      #imm, rs1 = 20, t0

        imm = binary_to_specified_len(int(imm),12)      #converting immediate value to 12bit binary string

        final = imm[-12:-5] + register_address[rs2] + register_address[rs1] + S_encoding.S_funct3[operation] + imm[-5:] + S_encoding.S_oppcode

        out.append(final)

    # U-Type Instruction
    elif operation in U_encoding.U_operations:

        rd,imm = inp[1].split(',')      #splitting to get for example rd, imm = t0, 20

        imm = binary_to_specified_len(int(imm),32) #Converting immediate value to 32 bits binary string
    
        val = registers[rd].value
        # if (operation == "lui"):
        #         registers[rd].val = 

        final = imm[-32:-12] + register_address[rd] + U_encoding.U_oppcode[operation]

        out.append(final)

    pc+=4 # Always keep this at the last of the loop!!!
    

assembly.close()

# Outputting to a txt file for now....

output = open(output_file,"w")

line_counter = 1
for x in out:
    if line_counter == no_of_lines:
        output.write(x)
    else:
        line_counter+=1
        output.write(x+"\n")
output.close()