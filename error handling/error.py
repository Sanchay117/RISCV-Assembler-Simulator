import Encoding.R_encoding as R_encoding
import Encoding.I_encoding as I_encoding
import Encoding.S_encoding as S_encoding
import Encoding.B_encoding as B_encoding
import Encoding.U_encoding as U_encoding
import Encoding.J_encoding as J_encoding
def check_instrction(instruction, valid_operations):
  # checking for operations
    if valid_operations not in R_operations or I_operations or S_operations or B_operations or U_operations or J_operations:
      return False
    else:
      return True
    # Check if there are exactly three registers (for R Type)
    # 
    #
    if len(instruction) != 3:
      return False
    else:
      return True
    # for I type, S Type, B Type
    #
    #
    if len(instruction) != 2: 
      return False
    else:
      return True
    # for U Type, J Type
    #
    #
    if len(instruction) != 1:
      return False
    else:
      return True
# Testing the function
input_string = input()
components = input_string.split(" ")
operation, registers = components[0], [comp.strip() for comp in components[1:]]
input_string = registers[0]
# Split the string by comma to get individual register names
register = input_string.split(",")
# Output each register name separated by comma and space
output_string = ", ".join(register)
if check_instrction(output_string, operation):
  print("Valid Instruction.")
else:
  print("Error")
