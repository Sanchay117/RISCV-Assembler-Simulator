S_oppcode="0100011"

S_funct3={"sw":"010"}
S_operations=["sw"]

def binary(n):
    n = int(n)
    if(n>=0):
        bin_string = bin(abs(n))   
        bin_string = bin_string[2:]
        bin_string = '0'*(12-len(bin_string)) + bin_string

    elif(n<0):
        bin_string = bin((abs(n)^((2**12)-1)) + 1)
        bin_string = bin_string[2:]
        bin_string = '1'*(12-len(bin_string)) + bin_string
    return bin_string
