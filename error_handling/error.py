from ..Encoding import R_encoding
from ..Encoding import I_encoding
from ..Encoding import S_encoding
from ..Encoding import B_encoding
from ..Encoding import U_encoding
from ..Encoding import J_encoding

# Now To Access Operations you can use R_encoding.R_operations
# what you have done is still ok but reduces the modularity of the code
# -Sanchay

def check_instruction(operation, operands):
    # Check if the operation is in the appropriate list
    if operation in R_encoding.R_operations or operation in I_encoding.I_operations or operation in B_encoding.B_operations:
        # For R, I, and B Type instructions, check if there are exactly three operands
        return len(operands) == 3
    elif operation in S_encoding.S_operations or operation in U_encoding.U_operations or operation in J_encoding.J_operations:
        # For S, U, and J Type instructions, check if there are exactly two operands
        return len(operands) == 2
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
