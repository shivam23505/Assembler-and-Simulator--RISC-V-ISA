# Assembler for RISC-V ISA 
import math
import binary_functions

#############################################################################################################
R_type_instructions  = ["add","sub","sll","slt","sltu","xor","srl","or","and"]
I_type_instructions  = ["lw","addi","sltiu","jalr"]
S_type_instructions  = ["sw"]
B_type_instructions  = ["beq","bne","blt","bge","bltu","bgeu"]
U_type_instructions  = ["lui","auipc"]
J_type_instuctions   = ["jal"]

registers_list = ["zero","ra","sp","gp","tp","t0","t1","t2","s0","s1","a0","a1","a2","a3","a4","a5","a6","a7"]
for i in range(2,12):
    s = "s"+str(i)
    registers_list.append(s)
for i in range(3,7):
    t= "t"+str(i)
    registers_list.append(t)

#The binary codes of all the registers required
registers_encoding = {}
for i in range(len(registers_list)):
    registers_encoding[registers_list[i]] = binary_functions.Binary_5_convert(i)

##############################################################################################################
def Rtype(instruction,r2,r1,rd): 
    #func7,r2,r1,func3,rd are strings
    opcodedefault = "0110011" # since it is same for all Rtype
    func3 ="";
    func7="";
    
    if instruction == "add":
        func7 = "0000000"
        func3 = "000"
    elif instruction == "sub":
        func7 = "0100000"
        func3 = "000"
        
    elif instruction == "sll":
        func7 = "0000000"
        func3 = "001"
        
    elif instruction == "slt":
        func7 = "0000000"
        func3 = "010"
        
    elif instruction == "sltu":
        func7 = "0000000"
        func3 = "011"
    elif instruction == "xor":
        func7 = "0000000"
        func3 = "100"
        
    elif instruction == "srl":
        func7 = "0000000"
        func3 = "101"
        
    elif instruction == "or":
        func7 = "0000000"
        func3 = "110"
        
    elif instruction == "and":
        func7 = "0000000"
        func3 = "111"
        
    rindex1 = str(registers_encoding[r1])
    rindex2 = str(registers_encoding[r2])
    rindexd = str(registers_encoding[rd])
    s1 = func7 + rindex2 + rindex1 + func3+ rindexd + opcodedefault
   
    return s1

def Rtype_error_checker(k):  # returns true if no error is found,k input string split around space
        parameters = k[1].split(",")
        for i in parameters: # checks if all registers passed valid
            if(str(i) in registers_list):
                continue;
            else:
                return False
        if(k[0] in R_type_instructions):
            pass
        
        else:
             return False
            
        if(len(parameters) != 3 or len(k)!=2):
             return False
        return True