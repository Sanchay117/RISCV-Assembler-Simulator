from R_encoding import R_operations
from I_encoding import I_operations
from S_encoding import S_operations
from B_encoding import B_operations
from U_encoding import U_operations
from J_encoding import J_operations
def check_instruction(operation, operands):
    # Check if the operation is in the appropriate list
    if operation in R_operations:
        # For R Type instructions, check if there are exactly three operands
        return len(operands) == 3
    elif operation in I_operations or operation in S_operations or operation in B_operations:
        # For I, S, and B Type instructions, check if there are exactly two operands
        return len(operands) == 2
    elif operation in U_operations or operation in J_operations:
        # For U and J Type instructions, check if there is exactly one operand
        return len(operands) == 1
    else:
        # If the operation is not recognized, return False
        return False

# Testing the function
input_string = input("Enter the instruction: ")
components = input_string.split(" ")
operation, operands = components[0], [comp.strip() for comp in components[1:]]
input_string = operands[0]
# Split the string by comma to get individual register names
register = input_string.split(",")
if check_instruction(operation, register):
    print("Valid Instruction.")
else:
    print("Invalid Instruction.")
