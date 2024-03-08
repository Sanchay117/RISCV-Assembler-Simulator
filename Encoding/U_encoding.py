U_operations=["lui","auipc"]

U_oppcode={
    "lui":"0110111",
    "auipc":"0010111"
}


def binary(n):
    n = int(n)
    if(n>=0):
        bin_string = bin(abs(n))
        bin_string = bin_string[2:]
        bin_string = '0'*(32-len(bin_string)) + bin_string

    elif(n<0):
        bin_string = bin((abs(n)^((2**32)-1)) + 1)
        bin_string = bin_string[2:]
        bin_string = '1'*(32-len(bin_string)) + bin_string
    return bin_string