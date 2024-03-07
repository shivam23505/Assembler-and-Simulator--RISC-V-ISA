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
def Stype_instruction(t):
    opcode = "0100011"
    funct3 = "010"
    imm_binary = binary_functions.BinaryConverter(int(t[3]))
    bin_string = imm_binary[:8] + registers_encoding[t[2]] + registers_encoding[t[1]] + funct3 + imm_binary[8:] + opcode
    return bin_string

#To check the credibility of Stype instruction
#returns False if instruction syntax not according to rules
def Stype_error_checker(assembly_instruction):
    t1 = (-1,-1,-1,-1)
    if assembly_instruction[0]!="sw":
        return t1
    parameters  = assembly_instruction[1].split(",")
    if len(parameters)!=2:
        return t1
    source_reg1 = parameters[0]
    x=parameters[1].find("(")
    y=parameters[1].find(")")
    if (x==-1 or y==-1):
        return t1
    source_reg2 = parameters[1][x+1:y]
    immediate_val = parameters[1][:x]

    if source_reg1 not in registers_list or source_reg2 not in registers_list:
        return t1
    if int(immediate_val)<=pow(-2,11) or int(immediate_val)>(pow(2,11)-1):
        return t1
    return (assembly_instruction[0],source_reg1,source_reg2,immediate_val)

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
    s=binary_functions.BinaryConverter(imm)
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
    s=binary_functions.BinaryConverter(imm)
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

def Rtype(t):  
    instruction=t[0]
    rd=t[1]
    r1=t[2]
    r2 = t[3]
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
        flag = 0
        if(len(k)==2):
            parameters = k[1].split(",")
            for i in parameters: # checks if all registers passed valid
                if(str(i) in registers_list):
                     continue;
                else:
                     flag =1
                     
            if(k[0] in R_type_instructions):
                pass
        
            else:
                flag=1
            
            if(len(parameters) != 3):
                flag=1
             
        else:
            flag =1
        
        if(flag==0): # return in the form instruction code,rd,rs1,rs2
            tuple1 = (k[0],parameters[0],parameters[1],parameters[2])
            return tuple1
        
        if(flag==1):
            tuple1 = (-1,-1,-1,-1)
            return tuple1

def Jtype(t):
    opcode = "1101111"
    imm_binary = binary_functions.BinaryConverter(int(t[2]))
    imm_binary = binary_functions.sign_extension(imm_binary,20)
    bin_string = imm_binary[0] + imm_binary[10:] + imm_binary[10]+imm_binary[1:9]+ registers_encoding[t[1]] + opcode
    return bin_string

def Jtype_error_checker(assembly_instruction):
    t1=(-1,-1,-1,-1)
    if assembly_instruction[0]!="jal":
        return t1
    x=assembly_instruction[1].split(",")
    if len(x)!=2:
        return t1
    if (x[0] not in registers_list):
        return t1
    if int(x[1])<(-pow(2,20)) or int(x[1])>(pow(2,20)-1):
        return t1
    return (assembly_instruction[0],x[0],x[1])

def main_program():
    with open("input.txt") as f:
        data = f.readlines()
    for i in data:
        i.strip()
    Lables = {}
    results = []
    hlt = "beq zero,zero,0x00000000"
    if data[-1]!=hlt:
        print("Error: Line:",len(data),"-->VIrtual Halt not at last")
        return
    pc = 0
    for i in range(len(data)-1):
        if (":" in data[i]):
            current_label = data[i][:(data[i].find(":"))]
            data[i] = data[i][data[i].find(":")+1:]
            Lables[current_label] = pc
        elif data[i]=="\n":
            continue
        elif data[i] ==hlt:
            print("Error at Line:",i+1,"-->VIrtual Halt twice")
            return
        pc+=4
        
    pc  = 0
    for i in range(len(data)-1):
        if data[i]=="\n":
            pass
        else:
            k  = data[i].split()
            ans_string = ""
            if Rtype_error_checker(k)[0]!=-1:
                ans_string  = Rtype(Rtype_error_checker(k))
            elif ierror(k)[0]!=-1:
                ans_string = Itype(ierror(k))
            elif Stype_error_checker(k)[0]!=-1:
                ans_string = Stype_instruction(Stype_error_checker(k))
            elif Jtype_error_checker(k)[0]!=-1:
                ans_string = Jtype(Jtype_error_checker(k))
            elif uerror(k)[0]!=-1:
                ans_string = UType(uerror(k))
            #elif Btype_error_checker(k)[0]!=-1:
            #    ans_string = Btype(k)
            else:
                print("Error at line:",i+1,"Invalid Instruction")
                return

            results.append(ans_string)
            pc+=4   

    with open("output.txt","a") as out:
        for i in results:
            if i==len(results)-1:
                out.write(i)
            else:
                out.write(i+"\n")
    print(Lables)
        
main_program()
def Btype(inst,t,imm):
    s0=binary_functions.BinaryConverter(imm)
    s=s0[12]+s0[10:4:-1]
    s2=s0[11]+s0[4:0:-1]
    opcode="1100011"
    if inst=="beq":
        funct3="000"
        result=s+t[1]+t[0]+funct3+s2+opcode
    elif inst=="bne":
        funct3="001"
        result=s+t[1]+t[0]+funct3+s2+opcode
    elif inst=="blt":
        funct3="100"
        result=s+t[1]+t[0]+funct3+s2+opcode
    elif inst=="bge":
        funct3="101"
        result=s+t[1]+t[0]+funct3+s2+opcode
    elif inst=="bltu":
        funct3="110"
        result=s+t[1]+t[0]+funct3+s2+opcode
    elif inst=="bgeu":
        funct3="111"
        result=s+t[1]+t[0]+funct3+s2+opcode
    return result
def B_error_checker(h):#eg:h=[inst,"t,imm"]
    if h[0] not in ["beq","bne","blt","bge","bltu","bgeu"]:
        return (-1,-1,-1,-1)
    y=h[1].split(",")
    x=y[0].split(",")
    if len(x)!=2:
        return (-1,-1,-1,-1)
    if x[0] and x[1] not in registers_list:
        return (-1,-1,-1,-1)
    if int(y[1])<=pow(-2,11) or int(y[1])>(pow(2,11)-1):
        return (-1,-1,-1,-1)
    return (h[0],[x[0],x[1]],y[1])
    
        
