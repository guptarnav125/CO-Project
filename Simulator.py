import sys

registers={
'00000': 0 ,
'00001': 0 ,
'00010': 0 ,
'00011': 0 ,
'00100': 0 ,
'00101': 0 ,
'00110': 0 ,
'00111': 0 ,
'01000': 0 ,
'01001': 0 ,
'01010': 0 ,
'01011': 0 ,
'01100': 0 ,
'01101': 0 ,
'01110': 0 ,
'01111': 0 ,
'10000': 0 ,
'10001': 0 ,
'10010': 0 ,
'10011': 0 ,
'10100': 0 ,
'10101': 0 ,
'10110': 0 ,
'10111': 0 ,
'11000': 0 ,
'11001': 0 ,
'11010': 0 ,
'11011': 0 ,
'11100': 0 ,
'11101': 0 ,
'11110': 0 ,
'11111': 0 
}

opcodes={
    '0110011':'R',
    '0000011':'I',
    '0010011':'I',
    '1100111':'I',
    '0100011':'S',
    '1100011': 'B',
    '0110111':'U',
    '0010111':'U',
    '1101111':'J'
}

memory={
    0x00010000:0b00000000000000000000000000000000,
    0x00010004:0b00000000000000000000000000000000,
    0x00010008:0b00000000000000000000000000000000,
    0x0001000c:0b00000000000000000000000000000000,
    0x00010010:0b00000000000000000000000000000000,
    0x00010014:0b00000000000000000000000000000000,
    0x00010018:0b00000000000000000000000000000000,
    0x0001001c:0b00000000000000000000000000000000,
    0x00010020:0b00000000000000000000000000000000,
    0x00010024:0b00000000000000000000000000000000,
    0x00010028:0b00000000000000000000000000000000,
    0x0001002c:0b00000000000000000000000000000000,
    0x00010030:0b00000000000000000000000000000000,
    0x00010034:0b00000000000000000000000000000000,
    0x00010038:0b00000000000000000000000000000000,
    0x0001003c:0b00000000000000000000000000000000,
    0x00010040:0b00000000000000000000000000000000,
    0x00010044:0b00000000000000000000000000000000,
    0x00010048:0b00000000000000000000000000000000,
    0x0001004c:0b00000000000000000000000000000000,
    0x00010050:0b00000000000000000000000000000000,
    0x00010054:0b00000000000000000000000000000000,
    0x00010058:0b00000000000000000000000000000000,
    0x0001005c:0b00000000000000000000000000000000,
    0x00010060:0b00000000000000000000000000000000,
    0x00010064:0b00000000000000000000000000000000,
    0x00010068:0b00000000000000000000000000000000,
    0x0001006c:0b00000000000000000000000000000000,
    0x00010070:0b00000000000000000000000000000000,
    0x00010074:0b00000000000000000000000000000000,
    0x00010078:0b00000000000000000000000000000000,
    0x0001007c:0b00000000000000000000000000000000
}

f=open(sys.argv[1],"r")
a=f.readlines()
for i in a:
    i=i.strip()
f.close()

#make a dictionary for program counter storing the statements as its values
PC={}
x=0
for i in a:
    PC[x]=i
    x+=4

def sext(value, bits):
    if value & (1 << (bits - 1)):
        return value - (1 << bits)
    else:
        return value
    
def R_type(funct7,rs2,rs1,funct3,rd):
    if funct7=="0000000" and funct3=="000": #add
        registers[rd]=registers[rs1]+registers[rs2]
    elif funct7=="0100000" and funct3=="000": #subtract
        registers[rd]=registers[rs1]-registers[rs2]
    elif funct3=="001": #sll
        xyz=registers[rs2]& 0b11111
        registers[rd]=registers[rs1]<<xyz
    elif funct3=="010": #slt
        if sext(registers[rs1],32)<sext(registers[rs2],32):
            registers[rd]=1
    elif funct3=="011": #sltu
        if registers[rs1]<registers[rs2]:
            registers[rd]=1
    elif funct3=="100": #xor
        registers[rd]=registers[rs1]^registers[rs2]
    elif funct3=="101": #srl
        xyz=registers[rs2]& 0b11111
        registers[rd]=registers[rs1]>>xyz
    elif funct3=="110":#or
        registers[rd]=registers[rs1]|registers[rs2]
    elif funct3=="111":#and
        registers[rd]=registers[rs1]&registers[rs2]

def I_type(imm,rs1,funct3,rd,opcode,counter):
    if funct3=="010": #lw
        xyz=registers[rs1]+sext(int(imm,2),32)
        registers[rd]=memory[hex(xyz)]
    elif funct3=="000" and opcode=="0010011": #addi
        registers[rd]=registers[rs1]+sext(int(imm,2),32)
    elif funct3=="011": #sltiu
        if registers[rs1]<int(imm,2):
            registers[rd]=1
    elif funct3=="000" and opcode=="1100111": #jalr
        registers[rd]=counter+4
        counter=(registers['00110']+sext(int(imm,2),32))& ~1
        global y
        y=counter

def S_type(imms1,rs2,rs1,funct3,imms2,opcode):
    if opcode == "0100011": #sw
        immtotal = imms1 + imms2
        storeval = registers[rs1] + sext(int(immtotal,2),32)
        memory[hex(storeval)] =registers[rs2]

def B_type(imm,rs2,rs1,funct3,counter):
    global y
    if funct3=="000": #beq
        if sext(registers[rs1],32)==sext(registers[rs2],32):
            y=counter+sext(int(imm,2),32)
    elif funct3=="001": #bne
        if sext(registers[rs1],32)!=sext(registers[rs2],32):
            y=counter+sext(int(imm,2),32)
    elif funct3=="100": #blt
        if sext(registers[rs1],32)<sext(registers[rs2],32):
            y=counter+sext(int(imm,2),32)
    elif funct3=="101": #bge
        if sext(registers[rs1],32)>=sext(registers[rs2],32):
            y=counter+sext(int(imm,2),32)
    elif funct3=="110": #bltu
        if registers[rs1]<registers[rs2]:
            y=counter+sext(int(imm,2),32)
    elif funct3=="111": #bgeu
        if registers[rs1]>=registers[rs2]:
            y=counter+sext(int(imm,2),32)
    
def U_type(imm,rd,opcode,counter):
    if opcode=="0110111": #lui
        registers[rd]=counter+sext(int(imm,2),32)
    elif opcode=="0010111": #auipc
        registers[rd]=sext(int(imm,2),32)

def J_type(imm,rd,counter): #jal
    registers[rd]=counter+4
    counter=(counter+sext(int(imm,2),32))& ~1
    global y
    y=counter


def inst_type(opcode): #function to determine type of statement
    for i in opcodes:
        if i==opcode:
            return opcodes[i]
        

def execute(inst,counter): #execute binary statement
    type=inst_type(inst[25:32]) #determine type
    if type=="R":
        R_type(inst[0:7],inst[7:12],inst[12:17],inst[17:20],inst[20:25])
    elif type=="I":
        I_type(inst[0:12],inst[12:17],inst[17:20],inst[20:25],inst[25:32],counter)
    elif type=="S":
        S_type(inst[0:7],inst[7:12],inst[12:17],inst[17:20],inst[20:25],inst[25:32])
    elif type=="B":
        imm=inst[0]+inst[24]+inst[1:7]+inst[20:24]
        B_type(imm,inst[7:12],inst[12:17],inst[17:20],counter)
    elif type=="U":
        U_type(inst[0:20],inst[20:25],inst[25:32],counter)
    elif type=="J":
        imm=inst[0]+inst[12:20]+inst[11]+inst[1:11]
        J_type(imm,inst[20:25],counter)
    
f=open(sys.argv[2],"w")

y=0
while y<x:
    f.write('0b'+format(y,'032b')) #Write program counter
    f.write(" ")
    execute(PC[y],y)
    for i in registers: #Write values of registers
        f.write('0b'+format(registers[i],'032b')) 
        f.write(" ")
    y+=4
    f.write("\n")

for address, value in memory.items():
    f.write(f"0x{address:08x}:0b{value:032b}\n")  # Write memory address and value to output file

f.close()
