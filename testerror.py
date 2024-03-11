from Encoding import R_encoding
from Encoding import I_encoding
from Encoding import S_encoding
from Encoding import B_encoding
from Encoding import U_encoding
from Encoding import J_encoding

# Now To Access Operations you can use R_encoding.R_operations
# what you have done is still ok but reduces the modularity of the code
# -Sanchay

register_address = {
"zero": "00000",
"ra":"00001", 
"sp": "00010",
"gp": "00011",
"tp":"00100",
"t0":"00101",
"t1":"00110",
"t2":"00111",
"s0":"01000",
"fp":"01000",
"s1":"01001",
"a0":"01010",
"a1":"01011",
"a2":"01100",
"a3":"01101",
"a4":"01110",
"a5":"01111",
"a6":"10000",
"a7":"10001",
"s2":"10010",
"s3":"10011",
"s4":"10100",
"s5":"10101",
"s6":"10110",
"s7":"10111",
"s8":"11000",
"s9":"11001",
"s10":"11010",
"s11":"11011",
"t3":"11100",
"t4":"11101",
"t5":"11110",
"t6":"11111"
}

def check_register(reg:str):
    if reg not in register_address.keys():
        return False
    return True

def mainchecker(line:str):
    opcode, other = line.split()
    if opcode in R_encoding.R_operations or opcode in I_encoding.I_operations or opcode in B_encoding.B_operations:
        if opcode in R_encoding.R_operations:
            rd, rs1, rs2 = other.split(",")
            if check_register(rd) and check_register(rs1) and check_register(rs2):
                 return True, "register-not-found"
            else:
                return False, "typo"
        elif opcode in I_encoding.I_operations:
            if opcode == "lw": #lw s0,48(gp) error 
                rd,oth = other.split(",")
                if(not check_register(rd)):
                    return False, "register-not-found"
                num, rd = oth.split("(")
                rd=rd.rstrip(")")
                if(not check_register(rd)):
                    return False, "register-not-found"
                if int(num) >= -1 * 2**11 and int(num) <= (2**11-1):
                    return True, "ok"
                return False, "typo"
            else:
                rd,rs,num = other.split(",")
                if(not check_register(rd) or not check_register(rs)):
                    return False, "register-not-found"
                if int(num) >= -1 * 2**11 and int(num) <= (2**11-1):
                    return True, "ok"
                return False, "typo"
        else: #for b enconding
            rs1, rs2, num = other.split(",") 
            if(not check_register(rs1) or not check_register(rs2)):
                return False, "register-not-found"
            if int(num) >= -1 * 2**12 and int(num) <= (2**12-1):
                return True, "ok"
            return False, "typo"
    elif opcode in S_encoding.S_operations or opcode in U_encoding.U_operations or opcode in J_encoding.J_operations:
        if opcode in S_encoding.S_operations:
            rs2, other = other.split(",")
            num, rs1 = other.split("(")
            rs1 = rs1.rstrip(")")
            if(not check_register(rs1) or not check_register(rs2)):
                return False, "register-not-found"
            if int(num) >= -1 * 2**11 and int(num) <= (2**11-1):
                return True, "ok"
            return False, "typo"
        elif opcode in U_encoding.U_operations:
            rd, num = other.split(",")
            if(not check_register(rd)):
                return False, "register-not-found"
            if int(num) >= -2147483648 and int(num) <= (2147483647):
                return True, "ok"
            return False, "typo"
        else: #for j encoding
            rd, num = other.split(",")
            if(not check_register(rd)):
                return False, "register-not-found"
            if int(num) >= -1048576 and int(num) <= (1048575):
                return True, "ok"
            return False, "typo"
    else:
        return False, "opcode-not-found"

a = open("test_assembly.txt","r")
t = a.readlines()
for x in t:
    print(x,end=" ")
    print(mainchecker(x))
