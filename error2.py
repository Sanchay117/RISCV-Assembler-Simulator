from Encoding import R_encoding
from Encoding import I_encoding
from Encoding import S_encoding
from Encoding import B_encoding
from Encoding import U_encoding
from Encoding import J_encoding

def Check_valid_immediate(value, operation):
  # For I, S Type
  if operation in I_encoding.I_operations or operation in S_encoding.S_operations:
    # 12 bits immediate value ( -2^11 to 2^11 -1)
    if -2048 <= value <= 2047:
      return True
  # B type
  if operation in B_encoding.B_operations:
    # 13 bits immediate value (-2^12 to 2^12-1)
    if -4096<= value <= 4095:
      return True
  
  # U type
  if operation in U_encoding.U_operations:
    # 32 bits immediate value( -2^31 to 2^31 - 1)
    if -2147483648 <= value <= 2147483647:  #range = [-2^31, 2^31 -1]
      return True
    
  # J Type
  if operation in J_encoding.J_operations:
    # 21 bits immediate value ( -2^20 to 2^20 -1)
    if -1048576 <= value <= 1048575:
      return True

  return False
  
#
# we need to convert label to immediate
#_______________________________________#

# Testing the function
def main2(lines):
  components = lines.split(" ")
  # print(components)
  # print(components[1:])
  operation, operands = components[0], components[-1]
  operands = operands.split(',')
  # print(operands)
  if operation in I_encoding.I_operations:
        if operation == "lw":
            imm,other = operands[-1].split('(')
            if not Check_valid_immediate(int(imm), operation):
               return False
            
        else:
            imm = operands[-1] #gives us rd, rs1 and imm/offset
            if not Check_valid_immediate(int(imm), operation):
               return False
  elif operation in S_encoding.S_operations:
      imm,other = operands[-1].split('(')   #splitting to get for example: rs2, k =  t1, 20(t0)
      if not Check_valid_immediate(int(imm),operation):
         return False
  
  elif operation in B_encoding.B_operations or operation in U_encoding.U_operations or operation in J_encoding.J_operations:
     
      imm = operands[-1]
      if imm.isnumeric():
        if not Check_valid_immediate(int(imm),operation):
          return False
  return True


  # Split the string by comma and indexing the last element to get the immediate valu
