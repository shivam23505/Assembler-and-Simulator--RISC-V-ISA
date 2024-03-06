#Converting imm to 2's complement
#Return 12 BIT binary string
def BinaryConverter(imm):
    imm=int(imm)
    x=(pow(2,11))
    if imm<0:
        imm=x+imm
        s=""
        while imm!=0:
            s+=str(imm%2)
            imm=imm//2
        s=s[::-1]
        if(len(s)<12):
            m="1"*(12-len(s))
            s=m+s
    else:
        s=""
        while imm!=0:
            s+=str(imm%2)
            imm=imm//2
        s=s[::-1]
        if(len(s)<12):
            m="0"*(12-len(s))
            s=m+s
    return s
def ierror(k):#k=["instruction_code","rd,rs,imm"]
    x=k[1].split(",")
    if k[0] not in ["lw","addi","sltiu","jalr"]:
        return False
    elif k[0]=="lw":
        if x[0] not in registers_list:
            return False
        z=x[1].find("(")
        z_=x[1].find(")")
        if z==-1 or z_==-1:
            return False
        else:
            imm=x[1][0:z]
            if int(imm)<=pow(-2,11) or int(imm)>(pow(2,11)-1):
                return False
            rs=x[1][z+1:x[1].find(")")]
            if rs not in registers_list:
                return False
    else:
        if x[0] not in registers_list:
            return False
        if x[1] not in registers_list:
            return False
        if int(x[2])<=pow(-2,11) or int(x[2])>(pow(2,11)-1):
            return False
    return True
#passing arguement take care of lw
def Itype(InstructionCode,rd,rs,imm,pc):
    #InstructionCode is string, 
    #rd is binary string, rs is binary string
    #imm is integer/string
    #pc is integer
    s = binary_functions.BinaryConverter(imm)
    finalbin=""
    if InstructionCode=="lw":
        finalbin=s+rs+"010"+rd+"0000011"
        pc+=4
    elif InstructionCode=="addi":
        finalbin=s+rs+"000"+rd+"0010011"
        pc+=4
    elif InstructionCode=="sltiu":
        finalbin=s+rs+"011"+rd+"0010011"
        pc+=4
    elif InstructionCode=="jalr":
        finalbin=s+rs+"000"+rd+"1100111"
        pc+=4
    return finalbin
def uerror(k):#k=["instruction code","rd,imm"]
    if k[0] not in ["auipc","lui"]:
        return False
    else:
        x=k[1].split(",")
        if len(x)!=2:
            return False
        if x[0] not in registers_list:
            return False
        if int(x[1])<pow(-2,11) or int(x[1])>(pow(2,11)-1):
            return False
    return True
def UType(InstructionCode,rd,imm,pc):
    s=BinaryConverter(imm)+rd
    if InstructionCode=="lui":
        s=s+"0110111"
    else:
        s=s+"0010111"
    return s
