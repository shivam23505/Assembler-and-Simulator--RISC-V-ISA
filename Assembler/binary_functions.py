
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

#converts number into 5-bit binary
#returns 5-bit binary string
def Binary_5_convert(num):
    s=""
    while num!=0:
        s+=str(num%2)
        num = num//2
    if (len(s)<5):
        m = "0"*(5-len(s))
        s= m + s
    return s