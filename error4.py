from Encoding import R_encoding
from Encoding import I_encoding
from Encoding import S_encoding
from Encoding import B_encoding
from Encoding import U_encoding
from Encoding import J_encoding

def check_rd(rd):
    if rd != "zero":
        return True
    else:
        return False

def main4(lines):
    components = lines.split(" ")
    operation, operands = components[0], [comp.strip() for comp in components[1:]]
    input_string = operands[0]
    # Split the string by comma to get individual register names
    register = input_string.split(",")
    rd = register[0]
    if check_rd(rd):
        print("Valid instruction")
    else:
        print("Invalid instruction")
