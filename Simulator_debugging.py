import Encoding.R_encoding as R_encoding
import Encoding.I_encoding as I_encoding
import Encoding.S_encoding as S_encoding
import Encoding.B_encoding as B_encoding
import Encoding.U_encoding as U_encoding
import Encoding.J_encoding as J_encoding
import sys
import time
def binary_to_specified_len(bin,l):
    return (bin[0]*(l-len(bin))) + bin

def twos_complement(x):
    '''
    Returns the 2's complement of `x`'
    :param x:
    :return: y
    '''
    y=''
    ind = 0
    for i in range(len(x)-1, -1, -1):
        if x[i] == '1':
            ind = i
            break
    for i in range(ind):
        if x[i] == '1':
            y+="0"
        else:
            y+="1"
    y+=x[ind:]
    return y

def two_complement_addition(a, b):
    # assumes both operands are of same length
    x=len(a)
    result=''
    carry=0
    for i in range(x-1,-1,-1):
        res = carry
        res += 1 if a[i] == '1' else 0
        res += 1 if b[i] == '1' else 0
        result = ('1' if res % 2 == 1 else '0') + result
        carry = 0 if res < 2 else 1
    return result

def two_complement_subtraction(a, b):
    '''
    Returns the 2's complement of `x`'
    :param a:
    :param b:
    :return:
    '''
    # performing a + (-b)
    two_complement_of_b=twos_complement( b) # this is -b
    return two_complement_addition(a,two_complement_of_b)

def two_comp_to_base_10(x):
    if x[0]=='1': # Negative Number
        return -1*int(twos_complement(x),2)
    else:
        return int(x,2)
    
def int_to_binary(number):
    if number == 0:
        return "0"  
    if number < 0:
        print("Negative number")
        sys.exit()
    binary = ""
    fraction = number - int(number)
    integer_part = abs(int(number))
    while integer_part > 0:
        binary = str(integer_part % 2) + binary
        integer_part //= 2
    max_digits = 16  
    while fraction > 0 and len(binary) <= max_digits:
        fraction *= 2
        bit = int(fraction)
        binary += str(bit)
        fraction -= bit
    return binary
counter = 1
def print_register():
    global counter
    print("Counter is - ", counter)
    counter+=1
    for reg in registers.values():
        print(reg.address+"->"+reg.value,end=" ")
    print('\n')
input_file,output_file = sys.argv[1],sys.argv[2]

from registers import Register,register_address

registers={}
for register_val in register_address.values():
    registers[register_val] = Register(register_val)
registers["00010"].value = "00000000000000000000000100000000"  #value of register sp
memory={
    "0x00010000":"0"*32,
    "0x00010004":"0"*32,
    "0x00010008":"0"*32,
    "0x0001000c":"0"*32,
    "0x00010010":"0"*32,
    "0x00010014":"0"*32,
    "0x00010018":"0"*32,
    "0x0001001c":"0"*32,
    "0x00010020":"0"*32,
    "0x00010024":"0"*32,
    "0x00010028":"0"*32,
    "0x0001002c":"0"*32,
    "0x00010030":"0"*32,
    "0x00010034":"0"*32,
    "0x00010038":"0"*32,
    "0x0001003c":"0"*32,
    "0x00010040":"0"*32,
    "0x00010044":"0"*32,
    "0x00010048":"0"*32,
    "0x0001004c":"0"*32,
    "0x00010050":"0"*32,
    "0x00010054":"0"*32,
    "0x00010058":"0"*32,
    "0x0001005c":"0"*32,
    "0x00010060":"0"*32,
    "0x00010064":"0"*32,
    "0x00010068":"0"*32,
    "0x0001006c":"0"*32,
    "0x00010070":"0"*32,
    "0x00010074":"0"*32,
    "0x00010078":"0"*32,
    "0x0001007c":"0"*32,
}

inp=open(input_file,'r')
lines=inp.readlines()
inp.close()

out =  []
line_out = []

pc = 0 # programm counter

while pc < len(lines)*4:

    print("R19 ",registers["10011"].value)
    line=lines[int(pc/4)]
    line=line.strip()
    # if line == "00000000000000000000000001100011":
    #     break
    oppcode=line[25:32] #line has  \n in last
    #print(len(lines)*4)
    print("flag 1")
    if oppcode == R_encoding.R_oppcode:
        print("PC->",pc)
        print("R TYPE EXECUTING",end='->')
        # to be done by sanchay

        funct7,funct3 = line[0:7],line[17:20]

        rs2,rs1,rd=line[7:12],line[12:17],line[20:25]

        a=registers[rs1].value
        b=registers[rs2].value

        a_value=two_comp_to_base_10(a)
        b_value=two_comp_to_base_10(b)

        a_unsigned=int(a,2)
        b_unsigned=int(b,2)


        if funct7 == R_encoding.R_funct7["add"] and funct3 == R_encoding.R_funct3["add"]:
            # think abt overflow....
            print("add")
            c=two_complement_addition(a,b)
            registers[rd].value=c
        if funct7==R_encoding.R_funct7["sub"] and funct3 == R_encoding.R_funct3["sub"]:
            print("sub")
            c=two_complement_subtraction(a,b)
            registers[rd].value=c
        if funct7==R_encoding.R_funct7["slt"] and funct3 == R_encoding.R_funct3["slt"]:
            print("slt",end='->')
            if a_value<b_value:
                registers[rd].value="0"*31 + "1"
                print("triggered",end="")
            print()
        if funct7==R_encoding.R_funct7["sltu"] and funct3 == R_encoding.R_funct3["sltu"]:
            print("sltu",end='->')
            if a_unsigned<b_unsigned:
                registers[rd].value="0"*31 + "1"
                print("triggered",end='')
            print()
        if funct7==R_encoding.R_funct7["xor"] and funct3 == R_encoding.R_funct3["xor"]:
            c=""
            for i in range(len(a)):
                if a[i]=='1' and b[i]=='1':
                    c+='0'
                elif a[i]=='1' or b[i]=='1':
                    c+='1'
                else:
                    c+='0'
            registers[rd].value=c
            print('xor')
        if funct7==R_encoding.R_funct7["sll"] and funct3 == R_encoding.R_funct3["sll"]:
            c=""
            shift=int(b[-5:],2)
            c=a[shift:]+("0"*shift)
            registers[rd].value=c
            print("sll")
        if funct7==R_encoding.R_funct7["srl"] and funct3 == R_encoding.R_funct3["srl"]:
            shift=int(b[-5:],2)
            c=("0"*shift)+a[:(-1*shift)]
            registers[rd].value=c
            print("srl")
        if funct7==R_encoding.R_funct7["or"] and funct3 == R_encoding.R_funct3["or"]:
            c=""
            for i in range(len(a)):
                if a[i]=='1' or b[i]=='1':
                    c+='1'
                else:
                    c+='0'
            registers[rd].value=c
            print('or')
        if funct7==R_encoding.R_funct7["and"] and funct3 == R_encoding.R_funct3["and"]:
            c=""
            for i in range(len(a)):
                if a[i]=='1' and b[i]=='1':
                    c+='1'
                else:
                    c+='0'
            registers[rd].value=c
            print("and")
        print(print_register())

    if oppcode in I_encoding.I_oppcode.values():
        print("PC->",pc)
        print("I TYPE EXECUTING",end="->")
        # to be done by ramneek
        rd = line[20:25]
        extfun = line[17:20]
        rs1 = line[12:17]
        imm = line[0:12]
        imm = binary_to_specified_len(imm, 32)
        # print(registers[rs1].value)
        if oppcode == I_encoding.I_oppcode["lw"]:
            final_ans="0x000"+hex(two_comp_to_base_10(two_complement_addition(registers[rs1].value, imm)))[2:]
            registers[rd].value = memory[final_ans]
            print('lw')
        if oppcode == I_encoding.I_oppcode["addi"] and extfun == I_encoding.I_funct3["addi"]:
            final_ans = two_complement_addition(registers[rs1].value, imm)
            registers[rd].value=final_ans
            print("addi")
        if oppcode == I_encoding.I_oppcode["sltiu"] and extfun == I_encoding.I_funct3["sltiu"]:
            print("sltiu",end="->")
            if two_comp_to_base_10(registers[rs1].value)<two_comp_to_base_10(imm):
                registers[rd].value = 1
                print("triggered",end="")
            print('\n')
        if oppcode == I_encoding.I_oppcode["jalr"]:
            print(binary_to_specified_len('0'+bin(pc+4)[2:],32))
            registers[rd].value = binary_to_specified_len('0'+bin(pc+4)[2:],32)
            print(registers[rs1].value)
            print(imm)
            final_ans = two_complement_addition(registers[rs1].value, imm)
            print(final_ans)
            #make last digit zero
            final_ans=final_ans[0:31] + '0'
            print(final_ans)
            pc = two_comp_to_base_10(final_ans)
            print('jalr')
            print(print_register())
            registers["00000"].value="0"*32
            bin_pc = '0' + bin(pc)[2:]
            line_out = '0b' + binary_to_specified_len(bin_pc,32) + ' '

            for register in registers:
                line_out += '0b'+registers[register].value+' '

            line_out.rstrip(' ')
            out += [line_out]
            print("Ending the instruction")

            continue
            # print('jalr')
        print(print_register())
        # print("PC->",pc)

    if oppcode == S_encoding.S_oppcode:
        print("PC->",pc)
        print("S TYPE EXECUTING",end="->")
        # to be done by pranav
        if oppcode == S_encoding.S_oppcode:
            # sw rs2, imm[11:0](rs1)
            print("sw")
            rs2,rs1,imm = line[-25:-20],line[-20:-15],line[-32:-25] + line[-12:-7]
        
            memory_address = two_comp_to_base_10(registers[rs1].value) + two_comp_to_base_10(imm)
            memory_address = "0x000" + hex(memory_address)[2:]

            memory[memory_address] = binary_to_specified_len(registers[rs2].value,32)
        print(print_register())

    

    if oppcode == B_encoding.B_oppcode:
        print("B TYPE EXECUTING")
        print("PC->",pc)
        # to be done by sanchay
        imm=line[0] + line[-8] + line[-31:-25] + line[-12:-8] + "0"
        funct3=line[-15:-12]
        rs2=line[-25:-20]
        rs1=line[-20:-15]
        print(rs1, rs2)
        print(two_comp_to_base_10(registers[rs1].value))
        rs2_val=two_comp_to_base_10(registers[rs2].value)
        rs1_val=two_comp_to_base_10(registers[rs1].value)
        # print(rs1_val,rs2_val)
        rs1_unsigned=int(registers[rs1].value,2)
        rs2_unsigned=int(registers[rs2].value,2)

        if funct3 == B_encoding.B_funct3["beq"]:
            print("Beq")
            if(rs1_val==rs2_val):
                if(two_comp_to_base_10(imm) != 0):
                    pc+=two_comp_to_base_10(binary_to_specified_len(imm,32))
                    # print(pc)
                    out+=[out[-1]]
                    print_register()
                    continue
                else:
                    # out+=[out[-1]]
                    # print_register()
                    print("Breaked over")
                    break

        if funct3 == B_encoding.B_funct3["bne"]:
            print("bne")
            if(rs1_val!=rs2_val):
                print("Condn triggered")
                print(rs1_val,rs2_val)
                pc+=two_comp_to_base_10(binary_to_specified_len(imm,32))
                print(pc)
                out+=[out[-1]]
                print_register()
                continue
            else:
                print_register()
                print("Condn not triggered")
        if funct3 == B_encoding.B_funct3["bge"]:
            print('bge')
            if(rs1_val>=rs2_val):
                pc+=two_comp_to_base_10(binary_to_specified_len(imm,32))
                out+=[out[-1]]
                print_register()
                continue
            print_register()
        if funct3 == B_encoding.B_funct3["bgeu"]:
            print("bgeu")
            if(rs1_unsigned>=rs2_unsigned):
                pc+=two_comp_to_base_10(binary_to_specified_len(imm,32))
                out+=[out[-1]]
                print_register()
                continue
            print_register()
        if funct3 == B_encoding.B_funct3["blt"]:
            print("blt")
            if(rs1_val<rs2_val):
                pc+=two_comp_to_base_10(binary_to_specified_len(imm,32))
                out+=[out[-1]]
                print_register()
                continue
            print_register()
        if funct3 == B_encoding.B_funct3["bltu"]:
            print("bltu")
            if(rs1_unsigned<rs2_unsigned):
                pc+=two_comp_to_base_10(binary_to_specified_len(imm,32))
                out+=[out[-1]]
                print_register()
                continue
            print_register()
        # what if pc increase lets say currently we at 0 but a B instruction causes it to get 8
        # so now do we straight away goto 8 or do we go to 12 because pc+=4 after every iteration?
        # print(pc)

    if oppcode in U_encoding.U_oppcode.values():
        # to be done by pranav
        print("PC->",pc)
        print("U TYPE EXECUTING",end="->")


        if oppcode == U_encoding.U_oppcode:
        

            rd = line[-12:-7]
            imm = line[-32:-12]
            if(oppcode == "0010111"):
            # auipc rd, imm[31:12]
                print("auipc")
                val1 = bin(pc)[2:]   #converting integer PC to 2's complement
                val1 = binary_to_specified_len(val1,32)   #Extending binary PC to 32 bits
  
                val2 = binary_to_specified_len(imm,32)  #Extending binary_immediate to 32 bits

                sum = two_complement_addition(val1, val2) # Adding both values
                registers[rd].value = sum   #storing value in register rd


            if(oppcode == "0110111"):
                print("lui")
                val = binary_to_specified_len(imm,32)   #Extending binary_imm to 32 bits
                registers[rd].value = val               #Storing 32 bit value in register rd
            print(print_register())


    if oppcode == J_encoding.J_oppcode:
        print("PC->",pc)
        # done by nischay
        print("J TYPE EXECUTING",end="->")
        print("jal")
        imm = line[0] + line[12:20]  + line[11] +line[1:11] #imm[20:1]
        rd = line[20:25]
        # ret_add = pc + 4
        ret_add ='0' + bin(pc + 4)[2:]
        print(ret_add)
        ret_add = binary_to_specified_len(ret_add, 32)
        registers[rd].value = ret_add
        temp_pc = pc
        #rd = ret_add
        ##PC = PC + sext({imm[20:1],1'b0})
        imm_bits = imm + '0'  # '1b0' added to imm_bits extending it to 21 bits
        # extended_imm = binary_to_specified_len((imm_bits), 32)  # Perform sign extension with LSB=0
        pc += two_comp_to_base_10(imm_bits)
        print(pc)
        print(print_register())
        registers["00000"].value="0"*32
        bin_pc = '0' + bin(pc)[2:]
        line_out = '0b' + binary_to_specified_len(bin_pc,32) + ' '
        print(line_out)
        for register in registers:
            line_out += '0b'+registers[register].value+' '

        line_out.rstrip(' ')
        out += [line_out]
        print("Ending the instruction")
        continue

    registers["00000"].value="0"*32
    bin_pc = '0' + bin(pc+4)[2:]
    line_out = '0b' + binary_to_specified_len(bin_pc,32) + ' '

    for register in registers:
        line_out += '0b'+registers[register].value+' '

    line_out.rstrip(' ')
    out += [line_out]
    print("Ending the instruction")
    pc += 4
    # time.sleep(0.2)
    
    

for location in memory:
    out += [location + ":0b"+ memory[location]]

output = open(output_file,"w")

for x in out:
    output.write(x+'\n')
# for x in out:
#     if(out.index(x) == len(out)-1):
#         output.write(x)
#     else:
#         output.write(x + '\n')

output.close()

