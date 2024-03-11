
    # Assembler for RISC-V ISA 
import math
import binary_functions
import sys
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

Lables = {}
##############################################################################################################
    
#Converting the S-type instructions into binary
#Syntax -- {instruction_code}{space}{return_address_reg}{,}{Source_reg}{,}{imm[11:0]}
#All the parameters are in string data type
def Stype_instruction(t):
    opcode = "0100011"
    funct3 = "010"
    imm_binary = binary_functions.BinaryConverter(int(t[3]))
    bin_string = imm_binary[:7] + registers_encoding[t[1]] + registers_encoding[t[2]] + funct3 + imm_binary[7:] + opcode
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
    if len(parameters[1])-1!=y:
        return t1
    if (x==-1 or y==-1):
        return t1
    source_reg2 = parameters[1][x+1:y]
    immediate_val = parameters[1][:x]

    if source_reg1 not in registers_list or source_reg2 not in registers_list:
        return t1
    if int(immediate_val)<pow(-2,31) or int(immediate_val)>(pow(2,31)-1):
        return t1
    return (assembly_instruction[0],source_reg1,source_reg2,immediate_val)

def ierror(k):#k=["instruction_code","rd,rs,imm"]
    
    if(len(k)==2):
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
                 if x[1][-1]!=")":
                    return(-1,-1,-1,-1)
            return ("lw",registers_encoding[x[0]],registers_encoding[rs],imm)
        else:
           if x[0] not in registers_list:
                return (-1,-1,-1,-1)
           if x[1] not in registers_list:
                return (-1,-1,-1,-1)
           if int(x[2])<=pow(-2,31) or int(x[2])>(pow(2,31)-1):
                return (-1,-1,-1,-1)
        return (k[0],registers_encoding[x[0]],registers_encoding[x[1]],x[2])
    else:
        return(-1,-1,-1,-1)
        


def uerror(k):#k=["instruction code","rd,imm"]
    if k[0] not in ["auipc","lui"]:
        return (-1,-1,-1,-1)
    else:
        x=k[1].split(",")
        if len(x)!=2:
            return (-1,-1,-1,-1)
        if x[0] not in registers_list:
            return (-1,-1,-1,-1)
        if int(x[1])<pow(-2,31) or int(x[1])>(pow(2,31)-1):
            return (-1,-1,-1,-1)
    return (k[0],registers_encoding[x[0]],int(x[1]))
def UType(t):#InstructionCode,rd,imm
    InstructionCode=t[0]
    rd=t[1]
    imm=t[2]
    s=binary_functions.BinaryConverter((imm))
    if int(imm)<0:
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
def Itype(t):#InstructionCode,rd,rs,imm
    #InstructionCode is string, 
    #rd is binary string, rs is binary string
    #imm is integer/string
    InstructionCode=t[0]
    rd=t[1]
    rs=t[2]
    imm=t[3]
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


def mulconvert(t):
    
    rd=t[1]
    r1=t[2]
    r2 = t[3]
    rindex1 = str(registers_encoding[r1])
    rindex2 = str(registers_encoding[r2])
    rindexd = str(registers_encoding[rd]) 
    s1 = "0111111"+ rindex2 + rindex1 +"000" + rindexd + "0000000"
   
    return s1

    

def mulerrorchecker(k):
    flag = 0
    if(len(k)==2):
            parameters = k[1].split(",")
            for i in parameters: # checks if all registers passed valid
                if(str(i) in registers_list):
                     continue;
                else:
                     flag =1
                     
            if(k[0]=="mul"):
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
    
    

        
        


def Jtype(t,pc):
    opcode = "1101111"
    if (t[2].isalpha()==False):
        destination  = t[2]
    else:
        destination = Lables[t[2]]-pc
    imm_binary = binary_functions.BinaryConverter(destination)
    imm_binary = binary_functions.sign_extension(imm_binary,21)
    bin_string = imm_binary[0] + imm_binary[10:20] + imm_binary[9]+imm_binary[1:9]+ registers_encoding[t[1]] + opcode
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
    if x[1].isalpha():
        if x[1] not in Lables:
            return t1
    else:
        if int(x[1])<(-pow(2,31)) or int(x[1])>(pow(2,31)-1):
            return t1
    return (assembly_instruction[0],x[0],x[1])


def Btype(k,pc):
    if k[3].isalpha()==False:
        destination = int(k[3])
    else:
        destination = Lables[k[3]]-pc
    s0=binary_functions.BinaryConverter(str(destination))
    s0 =binary_functions.sign_extension(s0,13)
    s=s0[0]+s0[2:8]
    s2=s0[8:12]+s0[1]
    opcode="1100011"
    if k[0]=="beq":
        funct3="000"
        result=s+registers_encoding[k[2]]+registers_encoding[k[1]]+funct3+s2+opcode
    elif k[0]=="bne":
        funct3="001"
        result=s+registers_encoding[k[2]]+registers_encoding[k[1]]+funct3+s2+opcode
    elif k[0]=="blt":
        funct3="100"
        result=s+registers_encoding[k[2]]+registers_encoding[k[1]]+funct3+s2+opcode
    elif k[0]=="bge":
        funct3="101"
        result=s+registers_encoding[k[2]]+registers_encoding[k[1]]+funct3+s2+opcode
    elif k[0]=="bltu":
        funct3="110"
        result=s+registers_encoding[k[2]]+registers_encoding[k[1]]+funct3+s2+opcode
    elif k[0]=="bgeu":
        funct3="111"
        result=s+registers_encoding[k[2]]+registers_encoding[k[1]]+funct3+s2+opcode
    return result

def B_error_checker(h):#eg:h=[inst,"t,imm"]
    if h[0] not in B_type_instructions:
        return (-1,-1,-1,-1)
    y=h[1].split(",")
    if len(y)!=3:
        return (-1,-1,-1,-1)
    if y[2].isalpha():
        if (y[0] not in registers_list) or (y[1] not in registers_list):
            return (-1,-1,-1,-1)
        if y[2] not in Lables:
            return (-1,-1,-1,-1)
    else:
        if int(y[2])<pow(-2,11) or int(y[2])>(pow(2,11)-1):
            return (-1,-1,-1,-1)
    return (h[0],y[0],y[1],y[2])
    

def bonus_type(t):
    rd=t[1]
    rs1=t[2]
    opcode="0011111"
    rdindex=str(registers_encoding[rd])
    rs1index=str(registers_encoding[rs1])
    result= "000000000000" + rs1index +"000"+ rdindex + opcode
    return result

def bonus_error(k):# k=["instructions","register1,register2"]
    if k[0] not in ["rvrs"]:
        return (-1,-1,-1,-1)
    x=k[1].split(",")
    if len(x)!=2:
        return (-1,-1,-1,-1)
    if x[0] not in registers_list and x[1] not in registers_list:
        return (-1,-1,-1,-1)
    return (k[0],x[0],x[1])   
     
        
def main_program(input_path,output_path):
    with open(input_path) as f:
        data = f.readlines()
    for i in data:
        i.strip()
    
    results = []
    hlt = "beq zero,zero,0"
    pc = 0
    for i in range(len(data)):
        if (":" in data[i]):
            current_label = data[i][:(data[i].find(":"))]
            data[i] = data[i][data[i].find(":")+1:]
            Lables[current_label] = pc
        elif data[i]=="\n":
            continue
        pc+=4
    flag = 0    
    pc  = 0
    for i in range(len(data)):
        
                
        if hlt in data[i]:
            flag=1
        if data[i]=="\n":
            pass
        else:
            
            k  = data[i].split()
            ans_string = ""
            if(k[0]=="halt"):
                ans_string= "1"*32
            elif k[0]=="rst":
                ans_string = "0"*32
            elif bonus_error(k)[0]!=-1:
                ans_string=bonus_type(bonus_error(k))
            elif Rtype_error_checker(k)[0]!=-1:
                ans_string  = Rtype(Rtype_error_checker(k))
            elif mulerrorchecker(k)[0]!=-1:
                ans_string  = mulconvert(mulerrorchecker(k))
            elif ierror(k)[0]!=-1:
                ans_string = Itype(ierror(k))
            elif Stype_error_checker(k)[0]!=-1:
                ans_string = Stype_instruction(Stype_error_checker(k))
            elif Jtype_error_checker(k)[0]!=-1:
                ans_string = Jtype(Jtype_error_checker(k),pc)
            elif uerror(k)[0]!=-1:
                ans_string = UType(uerror(k))
            elif B_error_checker(k)[0]!=-1:
                ans_string = Btype(B_error_checker(k),pc)
            else:
                print("Error at line:",i+1,"Invalid Instruction")
                return

            results.append(ans_string)
            pc+=4   
    if flag==0:
        print("ERROR: Virtual Hlt Missing")
        return
    with open(output_path,"w") as out: # w modes allows us to refresh output file 
        for i in results:
            out.write(i+"\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 Filename.py input_file_path output_file_path")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    main_program(input_path, output_path)
