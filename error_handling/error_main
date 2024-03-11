from ..Encoding import R_encoding
from ..Encoding import I_encoding
from ..Encoding import S_encoding
from ..Encoding import B_encoding
from ..Encoding import U_encoding
from ..Encoding import J_encoding

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

def lines_strip(line):
  return line.strip().split()

def check_instructions(operation, operands):
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
      
def check_instruction(tokens):
  operation = tokens[0]
  #print(operation)
  if operation in R_encoding.R_operations or operation in I_encoding.I_operations or operation in S_encoding.S_operations or operation in B_encoding.B_operations or operation in U_encoding.U_operations or operation in J_encoding.J_operations:
    return True
  else:
    return False

def check_lines(tokens, line_number):
  # Check for syntax errors
  if len(tokens) == 0:
    return "Empty line", line_number
  if len(tokens) == 1:
    return "Incomplete instruction", line_number
  if not check_instruction(tokens):
    return f"Invalid instruction '{tokens[0]}'", line_number
  if len(tokens) < 2:
    return f"Incomplete operands for '{tokens[0]}'", line_number
  return None, None

def Check_valid_immediate(value, operation):
  # For I, S, B Type
  if operation in I_encoding.I_operations or operation in S_encoding.S_operations or operation in B_encoding.B_operations:
    # 12 bits immediate value ( -2^11 to 2^11 -1)
    if -2048 <= value <= 2047:
      return True
  # For U, J Type
  if operation in U_encoding.U_operations or operation in J_encoding.J_operations:
    # 20 bits immediate value ( -2^19 to 2^19 -1)
    if -524288 <= value <= 524287:
      return True
  return False
  
#
# we need to convert label to immediate
#_______________________________________#

def main():
  with open("test_assembly.txt", "r") as file:
    lines = file.readlines()
    l = []
  for j in lines:
   if ":" in j:
    line_split = j.split(":")[1]
    l.append(line_split)
   if ":" not in j:
    l.append(j)
  # Check for errors and output error 
  error_found = False
  for i, line in enumerate(l, 1):
    tokens = lines_strip(line)
    error, error_line = check_lines(tokens, i)
    if error:
      print(f"Error: {error} at line {error_line}")
      error_found = True
      continue
  if not error_found:
    print("No errors found.")
  components = lines.split(" ")
  operation, operands = components[0], [comp.strip() for comp in components[1:]]
  input_string = operands[0]
  # Split the string by comma to get individual register names
  register = input_string.split(",")
  if check_registers(register):
    print(check_registers(register))
  else:
    if check_instructions(operation, register):
        print("Valid Instruction.")
    else:
        print("Invalid Instruction.")
  # Split the string by comma and indexing the last element to get the immediate value
  imm = (input_string.split(","))[-1]
  # in case of ex- lw a5,20(s1)
  immediate = (imm.split("("))[0]
  if Check_valid_immediate(int(immediate), operation):
    print("The immediate value is valid")
  else:
    print("The immediate value is invalid")

if __name__ == "__main__":
  main()
