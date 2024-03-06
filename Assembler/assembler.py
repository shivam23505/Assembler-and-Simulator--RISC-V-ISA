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

def ierror(k):#k=["instruction_code","rd,rs,imm"]
    x=k[1].split(",")
    if k[0] not in ["lw","addi","sltiu","jalr"]:
        return (-1,-1,-1,-1)
    elif k[0]=="lw":
        if x[0] not in registers_list:
            return (-1,-1,-1,-1)
        z=x[1].find("(")
        z_=x[1].find(")")
        if z==-1 or z_==-1:
            return (-1,-1,-1,-1)
        else:
            imm=x[1][0:z]
            if int(imm)<=pow(-2,11) or int(imm)>(pow(2,11)-1):
                return (-1,-1,-1,-1)
            rs=x[1][z+1:x[1].find(")")]
            if rs not in registers_list:
                return (-1,-1,-1,-1)
        return Itype("lw",x[0],rs,imm)
    else:
        if x[0] not in registers_list:
            return (-1,-1,-1,-1)
        if x[1] not in registers_list:
            return (-1,-1,-1,-1)
        if int(x[2])<=pow(-2,11) or int(x[2])>(pow(2,11)-1):
            return (-1,-1,-1,-1)
    return Itype(k[0],x[0],x[1],x[2])
def uerror(k):#k=["instruction code","rd,imm"]
    if k[0] not in ["auipc","lui"]:
        return (-1,-1,-1,-1)
    else:
        x=k[1].split(",")
        if len(x)!=2:
            return (-1,-1,-1,-1)
        if x[0] not in registers_list:
            return (-1,-1,-1,-1)
        if int(x[1])<pow(-2,11) or int(x[1])>(pow(2,11)-1):
            return (-1,-1,-1,-1)
    return (k[0],x[0],x[1])
def UType(InstructionCode,rd,imm):
    s=BinaryConverter(imm)
    if imm<0:
        s="1"*(32-len(s))+s
        s=s[0:20]+rd
    else:
        s="0"*(32-len(s))+s
        s=s[0:20]+rd
    if InstructionCode=="lui":
        s=s+"0110111"
    else:
        s=s+"0010111"
    return s
#passing arguement take care of lw
def Itype(InstructionCode,rd,rs,imm):
    #InstructionCode is string, 
    #rd is binary string, rs is binary string
    #imm is integer/string
    #pc is integer
    s=BinaryConverter(imm)
    finalbin=""
    if InstructionCode=="lw":
        finalbin=s+rs+"010"+rd+"0000011"
    elif InstructionCode=="addi":
        finalbin=s+rs+"000"+rd+"0010011"
    elif InstructionCode=="sltiu":
        finalbin=s+rs+"011"+rd+"0010011"
    elif InstructionCode=="jalr":
        finalbin=s+rs+"000"+rd+"1100111"
    return finalbin
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

def Jtype(inst_code,rd,imm):
    opcode = "1101111"
    imm_binary = binary_functions.BinaryConverter(int(imm))
    imm_binary = binary_functions.sign_extension(imm_binary,20)
    bin_string = imm_binary[0] + imm_binary[10:] + imm_binary[10]+imm_binary[1:9]+ rd + opcode
    return bin_string

def Jtype_error_checker(assembly_instruction):
    if assembly_instruction[0]!="jal":
        return False
    x=assembly_instruction[1].split(",")
    if len(x)!=2:
        return False
    if (x[0] not in registers_list):
        return False
    if int(x[1])<(-pow(2,20)) or int(x[1])>(pow(2,20)-1):
        return False
    return True

