def check_registers(instruction):
    # Splitting the instruction by commas
    registers = [reg.strip() for reg in instruction.split(',')]
    # Check if there are exactly three registers (for R Type)
    # 
    #
    if len(registers) != 3:
      return False
    else:
      return True
    # for I type, S Type, B Type
    #
    #
    if len(registers) != 2:
      return False
    else:
      return True
    # for U Type, J Type
    #
    #
    if len(registers) != 1:
      return False
    else:
      return True
# Testing the function
instruction = input("Enter the instruction: ")
if check_registers(instruction):
  print("All registers are present.")
else:
  print("Error")
