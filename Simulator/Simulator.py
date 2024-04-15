import math
import sys
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
for i in range(0,32):
    register[Binary_5_convert(i)]='0b'+'0'*32
register[Binary_5_convert(2)]='0b'+BinaryConverter(256)

def IntTo32Bitsigned(n):
    # if n < -2147483648 or n > 2147483647:
    #     raise ValueError("Input integer out of range for 32-bit 2's complement representation")    
    if n >= 0:
        binary_str = bin(n)[2:].zfill(32)
    else:
        binary_str = bin(2**32 + n)[2:]

    return binary_str

def Signedto32BitsInt(binary_str):
    # if len(binary_str) != 32:
    #     raise ValueError("Input string must be exactly 32 characters long")

    if binary_str[0] == '1':
        # If the most significant bit is 1, it's a negative number
        # Convert it to its negative equivalent
        negative_equivalent = int(binary_str, 2) - 2**32
        return negative_equivalent
    else:
        # If the most significant bit is 0, it's a non-negative number
        return int(binary_str, 2)
    
    
def Signedto32BitsIntU(binary_str):
    decimal_value = 0
    for i in range(len(binary_str)):
        if binary_str[i] == '1':
            decimal_value += 2**(31 - i)

    return decimal_value

def get_binary_representation(number):
    binary = ""
    for i in range(31, -1, -1):
        binary += "1" if number & (1 << i) else "0"
    return binary

def get_binary_representation5(number):
    binary = ""
    for i in range(4, -1, -1):
        binary += "1" if number & (1 << i) else "0"
    return binary

def binary_to_int(binary_str):
    # if len(binary_str) != 5:
    #     raise ValueError("Input string must be exactly 5 characters long")

    decimal_value = 0
    for i in range(len(binary_str)):
        if binary_str[i] == '1':
            decimal_value += 2**(4 - i)

    return decimal_value

# def binarytonumber(bin):
#     count=0
#     for i in range(0,31):
#         count=count+int(bin[i])*(pow(2,31-i))
def binarytonumber_two_complement(bin):
    count=0
    count=count+int(bin[0])*pow(2,len(bin)-1)*(-1)
    for i in range(1,len(bin)):
        count=count+int(bin[i])*(pow(2,len(bin)-1-i))
    return count
def Rtype(binary_input):
    global pc
    opcode = binary_input[25:len(binary_input)] #is used to extract the opcode
    func3 = binary_input[-15:-12]
    
    func7 = binary_input[0:7]
    rs2 = binary_input[7:12]
    rs1 = binary_input[12:17]
    rd = binary_input[20:25]
   
    rs2val = binarytonumber_two_complement(register[rs2][2:len(register[rs2])])
    rs1val = binarytonumber_two_complement(register[rs1][2:len(register[rs2])])
    rdval = binarytonumber_two_complement(register[rd][2:len(register[rd])])
    pc+=4

    
    if(func3 == "000" and func7 == "0000000"): # add function
        rdval = rs1val + rs2val
        register[rd] = "0b"+ BinaryConverter(rdval)
        return;
    
    if func7 == "0100000" and func3 =="000": # subtract
        rdval = rs1val - rs2val
        register[rd ] = "0b" + BinaryConverter(rdval)
        return
    
    if(func3 == "001" and func7 == "0000000"): #from l-5 to l sll instruction
        #  l =len( register[rs2]);
         tempstr = register[rs2][-5:] 
         rdval = rs1val << binary_to_int(tempstr)
         register[rd ] = "0b" + BinaryConverter(rdval)
         return 
     
    if(func3 == "101" and func7 == "0000000"): #from l-5 to l srl instruction        
        # l =len( register[rs2]);
        tempstr = register[rs2][-5:] 
        rdval = rs1val >> binary_to_int(tempstr)        
        register[rd ] = "0b" + BinaryConverter(rdval)        
        return 
    
    if(func3 == "110" and func7 == "0000000"): # or function        
        rdval = rs1val|rs2val
        register[rd ] = "0b" + BinaryConverter(rdval)        
        return
    
    if(func3 == "111" and func7 == "0000000"): # and function
        rdval = rs1val&rs2val
        register[rd ] = "0b" + BinaryConverter(rdval)        
        return
    
    if(func3 == "010" and func7 == "0000000"): # slt type        
        if(rs1val < rs2val):
            rdval = 1            
        else:
            rdval = 0            
        register[rd ] = "0b" + BinaryConverter(rdval)        
        return
    
    if(func3 == "011" and func7 == "0000000"): # slt type
        rs2val = Signedto32BitsIntU(register[rs2][2:len(register[rs2])])
        rs1val = Signedto32BitsIntU(register[rs1][2:len(register[rs2])])        
        if(rs1val < rs2val):
            rdval = 1            
        else:
            rdval = 0
        register[rd ] = "0b" + BinaryConverter(rdval)
        return
    
    if(func3 == "111" and func7 == "0000000"): #bitwise xor
        rdval = rs1val^rs2val
        register[rd ] = "0b" + BinaryConverter(rdval)
        return


def binarytonumber(bin):
    #bin is string
    return int(bin,2)

#print correct value of jalr in main
def itype(s):
    s=s[::-1]
    global pc
    imm=(s[31:19:-1])
    rs1=s[19:14:-1]
    func=s[14:11:-1]
    rd=s[11:6:-1]
    op=s[6::-1] 
    if op=="0000011":
    #convert the memory address into hexadecimal then get the value from the memory location
    #and do the rest of the work
        a= hex((binarytonumber_two_complement(register[rs1][2:]))+binarytonumber_two_complement(str(imm)))
        a=a[0:2] + "0"*(8-(len(a)-2)) + a[2:]
        register[rd]=memory_values[a]
    elif op=="0010011":
        register[rd]="0b"+BinaryConverter(binarytonumber_two_complement(register[rs1][2:])+binarytonumber_two_complement(str(imm)))
    else:
        # x=((binarytonumber(register["00111"][2:]))+binarytonumber(imm))
        # if(x%2==0):
        #     pc=pc+x
        # else:
        #     pc=pc+x-1
        pc=binarytonumber_two_complement(register[rs1][2:])
        return
    pc=pc+4

def Stype(binary_input):
    global pc
    imm = binary_input[:7] + binary_input[-12:-7]
    rs2 = binary_input[7:12]
    rs1 = binary_input[12:17]
    new_value = binarytonumber_two_complement(register[rs1][2:]) + binarytonumber_two_complement(imm)
    a= hex(new_value)
    a=a[0:2] + "0"*(8-(len(a)-2)) + a[2:]
    memory_values[a] = register[rs2] 
    pc+=4

def utype(binary_input):
    global pc
    opcode = binary_input[-7:]
    rd = binary_input[-12:-7]
    imm = binary_input[-32:-12]+12*"0"
    if opcode =="0010111":
        new_value = BinaryConverter(pc + binarytonumber_two_complement(imm))
        register[rd] = "0b"+new_value
    else:
        register[rd] = "0b" + imm
    pc+=4

def jtype(binary_input):
    global pc
    rd = binary_input[-12:-7]
    imm = binary_input[0]+binary_input[12:20]+binary_input[11]+binary_input[1:11] +"0"
    register[rd] ="0b" + BinaryConverter(pc+4)
    pc = pc + binarytonumber_two_complement(imm)


def btype(binary_input):
    global pc
    funct3 = binary_input[-15:-12]
    rs1 = binary_input [-20:-15]
    rs2 = binary_input[-25:-20]
    imm = binary_input[0] + binary_input[-8] + binary_input[1:7] +binary_input[-12:-8]+"0"
    value1 = binarytonumber_two_complement(register[rs1][2:])
    value2 = binarytonumber_two_complement(register[rs2][2:])
    match funct3:
        case "000":
            pc=(pc+binarytonumber_two_complement(imm)) if (value1==value2) else (pc+4)
        case "001":
            pc=(pc+binarytonumber_two_complement(imm)) if (value1!=value2) else (pc+4)
        case "100":
            pc=(pc+binarytonumber_two_complement(imm)) if (value1<value2) else (pc+4)
        case "101":
            pc=(pc+binarytonumber_two_complement(imm)) if (value1>=value2) else (pc+4)
        case "111":
            value_1 =int(register[rs1][2:],2)
            value_2 = int(register[rs2][2:],2)
            magnitude = int(imm[1:],2)
            if (imm[0]=="1"):
                magnitude=-magnitude
            pc = (pc+magnitude) if (value_1>=value_2) else (pc+4)
        case "110":
            value_1 =int(register[rs1][2:],2)
            value_2 = int(register[rs2][2:],2)
            magnitude = int(imm[1:],2)
            if (imm[0]=="1"):
                magnitude=-magnitude
            pc = (pc+magnitude) if (value_1<value_2) else (pc+4)
        case default:
            return 0

def print_reg_values():
    global pc
    ans = []
    ans.append("0b"+BinaryConverter(pc))
    for i in register.values():
        ans.append(i)
    return ans


def main_program(input_path,output_path):
    global pc
    with open(input_path) as f:
        data = f.readlines()
    for line in data:
        line.strip()
    halt = "0"*25+"1100011"
    solutions = []
    curr_instruction = data[pc//4]
    curr_instruction = curr_instruction[:-1]
    while (curr_instruction!=halt):
        # print(pc)
        curr_opcode = curr_instruction[25:32]
        if curr_opcode =="0110011":
            Rtype(curr_instruction)
        elif curr_opcode =="0100011":
            Stype(curr_instruction)
        elif curr_opcode =="1100011":
            btype(curr_instruction)
        elif curr_opcode == "1101111":
            jtype(curr_instruction)
        elif curr_opcode in ["0110111","0010111"]:
            utype(curr_instruction)
        else:
            itype(curr_instruction)

        solutions.append(" ".join(print_reg_values()))
        curr_instruction = data[pc//4]
        if (curr_instruction!=halt):
            curr_instruction = curr_instruction[:-1]
    # #after halt has been called print again the values
    solutions.append(" ".join(print_reg_values()))

    with open(output_path,"w") as out:
        for i in solutions:
            out.write(i+" \n")
        for i in range(len(memory_locations)-1):
            out.write(memory_locations[i]+":"+memory_values[memory_locations[i]]+"\n")
        out.write(memory_locations[-1]+":"+memory_values[memory_locations[-1]]+" ")


# main_program("input.txt","output.txt")
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 Filename.py input_file_path output_file_path")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    main_program(input_path, output_path)

