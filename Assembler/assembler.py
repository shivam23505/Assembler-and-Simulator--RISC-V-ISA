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
    
#Converting the S-type instructions into binary
#Syntax -- {instruction_code}{space}{return_address_reg}{,}{Source_reg}{,}{imm[11:0]}
#All the parameters are in string data type
def Stype_instruction(inst_code,rs1,rs2,imm):
    opcode = "0100011"
    funct3 = "010"
    imm_binary = binary_functions.BinaryConverter(int(imm))
    bin_string = imm_binary[:8] + rs2 + rs1 + funct3 + imm_binary[8:] + opcode
    return bin_string

#To check the credibility of Stype instruction
#returns False if instruction syntax not according to rules
def Stype_error_checker(assembly_instruction):
    if assembly_instruction[0]!="sw":
        return False
    parameters  = assembly_instruction[1].split(",")
    if len(parameters)!=2:
        return False
    source_reg1 = parameters[0]
    x=parameters[1].find("(")
    y=parameters[1].find(")")
    if (x==-1 or y==-1):
        return False
    source_reg2 = parameters[1][x+1:y]
    immediate_val = parameters[1][:x]

    if source_reg1 not in registers_list or source_reg2 not in registers_list:
        return False
    if int(immediate_val)<=pow(-2,11) or int(immediate_val)>(pow(2,11)-1):
        return False
    return True