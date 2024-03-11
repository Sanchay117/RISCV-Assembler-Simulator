from ..Encoding import R_encoding
from ..Encoding import I_encoding
from ..Encoding import S_encoding
from ..Encoding import B_encoding
from ..Encoding import U_encoding
from ..Encoding import J_encoding

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

def check_instruction(operation, operands):
    # Check if the operation is in the appropriate list
    if operation in R_encoding.R_operations or operation in I_encoding.I_operations or operation in B_encoding.B_operations:
        # For R, I, and B Type instructions, check if there are exactly three operands
        if operation == "lw":
            # As "lw" operation has only 2 operands.
          return len(operands) == 2
        return len(operands) == 3
    elif operation in S_encoding.S_operations or operation in U_encoding.U_operations or operation in J_encoding.J_operations:
        # For S, U, and J Type instructions, check if there are exactly two operands
        return len(operands) == 2
    else:
        # If the operation is not recognized, return False
        return False

def check_registers(register):
  for r in register:
  # check if the register is correct
    if r not in register_address.keys():
      return f"incorrect register {r}"

# Testing the function
input_string = input("Enter the instruction: ")
components = input_string.split(" ")
operation, operands = components[0], [comp.strip() for comp in components[1:]]
input_string = operands[0]
# Split the string by comma to get individual register names
register = input_string.split(",")
if check_registers(register):
  print(check_registers(register))
else:
  if check_instruction(operation, register):
      print("Valid Instruction.")
  else:
      print("Invalid Instruction.")
