#SIMULATOR FOR RISC-ISA V
opcode = {"Rtype":"0110011","Stype":"0100011","Btype":"1100011","Jtype":"1101111",
        "Utype":["0110111","0010111"],"Itype":["0000011","0010011","0010011","1100111"]}

memory_locations = ["0x00010000","0x00010004","0x00010008","0x0001000c","0x00010010","0x00010014","0x00010018","0x0001001c","0x00010020",
                    "0x00010024","0x00010028","0x0001002c","0x00010030","0x00010034","0x00010038","0x0001003c","0x00010040",
                    "0x00010044","0x00010048","0x0001004c","0x00010050","0x00010054","0x00010058","0x0001005c","0x00010060","0x00010064",
                    "0x00010068","0x0001006c","0x00010070","0x00010074","0x00010078","0x0001007c"]
memory_values = {}
for i in memory_locations:
    memory_values[i] = "0b" + "0"*32

#Registers dictionary to store the values of individual registers
#Format-- Registers = {"5_bitbinary":"0b"+"32bit_binary"}

program_counter = 0
def Jtype(binary_input):
    global program_counter
     


#main 
    #check by opcode
    #individual functions
    #change register/memory value
    #update program counter
    #until virtual halt
