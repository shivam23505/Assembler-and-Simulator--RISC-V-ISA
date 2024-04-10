import math
#SIMULATOR FOR RISC-ISA V
opcode = {"Rtype":"0110011","Stype":"0100011","Btype":"1100011","Jtype":"1101111",
        "Utype":["0110111","0010111"],"Itype":["0000011","0010011","0010011","1100111"]}

memory_locations = ["0x00010000","0x00010004","0x00010008","0x0001000c","0x00010010","0x00010014","0x00010018","0x0001001c","0x00010020",
                    "0x00010024","0x00010028","0x0001002c","0x00010030","0x00010034","0x00010038","0x0001003c","0x00010040",
                    "0x00010044","0x00010048","0x0001004c","0x00010050","0x00010054","0x00010058","0x0001005c","0x00010060","0x00010064",
                    "0x00010068","0x0001006c","0x00010070","0x00010074","0x00010078","0x0001007c"]
memory_values = {}
pc=0
for i in memory_locations:
    memory_values[i] = "0b" + "0"*32
def Binary_5_convert(num): 
    #num is integer
    #returns binary_string
    s=""
    while num!=0:
        m=str(num%2)
        s = m+s
        num = num//2
    if (len(s)<5):
        m = "0"*(5-len(s))
        s= m + s
    return s
def BinaryConverter(imm):
    #imm can be string or integer
    #returns string
    imm=int(imm)
    x=(pow(2,31))
    if imm<0:
        imm=x+imm
        s=""
        while imm!=0:
            s+=str(imm%2)
            imm=imm//2
        s=s[::-1]
        if(len(s)<32):
            m="1"*(32-len(s))
            s=m+s
    else:
        s=""
        while imm!=0:
            s+=str(imm%2)
            imm=imm//2
        s=s[::-1]
        if(len(s)<32):
            m="0"*(32-len(s))
            s=m+s
    return s
register={}
#Defining register from 0 to 31
for i in range(0,31):
    register[Binary_5_convert(i)]='0b'+'0'*32
register[Binary_5_convert(2)]='0b'+BinaryConverter(256)

def binarytonumber(bin):
    #bin is binary_string
    #returns the corresponding decimal
    count=0
    count=count+int(bin[0])*pow(2,len(bin)-1)*-1
    for i in range(1,len(bin)):
        count=count+int(bin[i])*(pow(2,len(bin)-1-i))
    return count
#print correct value of jalr in main
def itype(s):
    s=s[::-1]
    global pc
    imm=int(s[31:19:-1])
    rs1=s[19:14:-1]
    func=s[14:11:-1]
    rd=s[11:6:-1]
    op=s[6:-1:-1]
    if op=="0000011":
        register[rd]=memory_values[(binarytonumber(register[rs1[2:]]))+binarytonumber(imm)]
    elif op=="0010011":
        register[rd]="0b"+BinaryConverter(binarytonumber(register[rs1[2:]])+binarytonumber(imm))
    else:
        pc=binarytonumber(str(int(register["0b00111"])+binarytonumber(imm)))
    pc=pc+4

def Stype(binary_input):
    global pc
    imm = binary_input[:7] + binary_input[-12:-7]
    rs2 = binary_input[7:12]
    rs1 = binary_input[12:17]
    new_value = binarytonumber(register[rs1][2:]) + binarytonumber(imm)
    memory_values[BinaryConverter(new_value)] = register[rs2] 
    pc+=4

def utype(binary_input):
    opcode = binary_input[-7:]
    rd = binary_input[-12:-7]
    imm = binary_input[21:]+12*"0"
    if opcode =="0110111":
        new_value = BinaryConverter(pc + binarytonumber(imm))
        register[rd] = "0b"+new_value
    else:
        register[rd] = "0b" + imm
    pc+=4

def jtype(binary_input):
    rd = binary_input[-12:-7]
    imm = binary_input[0]+binary_input[12:]+binary_input[11]+binary_input[1:11] +"0"
    register[rd] ="0b" + BinaryConverter(pc+4)
    pc = pc + binarytonumber(imm)
