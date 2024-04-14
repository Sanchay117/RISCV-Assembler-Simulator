import Encoding.R_encoding as R_encoding
import Encoding.I_encoding as I_encoding
import Encoding.S_encoding as S_encoding
import Encoding.B_encoding as B_encoding
import Encoding.U_encoding as U_encoding
import Encoding.J_encoding as J_encoding
import sys

input_file,output_file = sys.argv[1],sys.argv[2]

from registers import Register,register_address

registers={}
for register in register_address.keys():
    registers[register] = Register(register_address[register])

inp=open(input_file,'r')
lines=inp.readlines()
inp.close()

for line in lines:
    oppcode=line[-7:]

    if oppcode == R_encoding.R_oppcode:
        # to be done by sanchay

        funct7,funct3 = line[0:8],line[17:20]

    if oppcode in I_encoding.I_oppcode.values():
        # to be done by ramneek
        pass

    if oppcode == S_encoding.S_oppcode:
        # to be done by pranav
        pass

    if oppcode == B_encoding.B_oppcode:
        # to be done by sanchay
        pass

    if oppcode in U_encoding.U_oppcode.values():
        # to be done by pranav
        pass

    if oppcode == J_encoding.J_oppcode:
        # to be done by nischay
        pass