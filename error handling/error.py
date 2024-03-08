import Encoding.R_encoding as R_encoding
import Encoding.I_encoding as I_encoding
import Encoding.S_encoding as S_encoding
import Encoding.B_encoding as B_encoding
import Encoding.U_encoding as U_encoding
import Encoding.J_encoding as J_encoding
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
