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