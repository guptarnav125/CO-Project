instruction_type={
    'add':'R',
    'sub':'R',
    'sll':'R',
    'slt':'R',
    'sltu':'R',
    'xor':'R',
    'srl':'R',
    'or':'R',
    'and':'R',
    'addi':'I',
    'lw':'I',
    'sltiu':'I',
    'jalr':'I',
    'sw':'S',
    'beq':'B',
    'bne':'B',
    'blt':'B',
    'bge':'B',
    'bltu':'B',
    'bgeu':'B',
    'lui':'U',
    'auipc':'U',
    'jal':'J'
}

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

OPCODES={
    'add':'0110011',
    'sub':'0110011',
    'sll':'0110011',
    'slt':'0110011',
    'sltu':'0110011',
    'xor':'0110011',
    'srl':'0110011',
    'or':'0110011',
    'and':'0110011',
    'addi':'0010011',
    'lw':'0000011',
    'sltiu':'0010011',
    'jalr':'1100111',
    'sw':'0100011',
    'beq':'1100011',
    'bne':'1100011',
    'blt':'1100011',
    'bge':'1100011',
    'bltu':'1100011',
    'bgeu':'1100011',
    'lui':'0110111',
    'auipc':'0010111',
    'jal':'1101111'
}

OPCODE_to_instruction_type={
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

f=open("input.txt","r")
a=f.readlines()
for i in a:
    i=i.strip()
f.close()

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
    
def execute_R_type(funct7,rs2,rs1,funct3,rd):
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

def execute_I_type(imm,rs1,funct3,rd,opcode,counter):
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

def execute_S_type(imms1,rs2,rs1,funct3,imms2,opcode):
    if opcode == "0100011":
        immtotal = imms1 + imms2
        storeval = registers[rs1] + sext(int(immtotal,2),32)
        memory[hex(storeval)] =registers[rs2]

def execute_B_type(imm,rs2,rs1,funct3,counter):
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
    
                   

def execute_U_type(imm,rd,opcode,counter):
    if opcode=="0110111": #lui
        registers[rd]=counter+sext(int(imm,2),32)
    elif opcode=="0010111": #auipc
        registers[rd]=sext(int(imm,2),32)

def execute_J_type(imm,rd,counter):
    registers[rd]=counter+4
    counter=(counter+sext(int(imm,2),32))& ~1
    global y
    y=counter


def inst_type(opcode):
    for i in OPCODE_to_instruction_type:
        if i==opcode:
            return OPCODE_to_instruction_type[i]
        

def execute(inst,counter):
    type=inst_type(inst[25:32])
    if type=="R":
        execute_R_type(inst[0:7],inst[7:12],inst[12:17],inst[17:20],inst[20:25])
    elif type=="I":
        execute_I_type(inst[0:12],inst[12:17],inst[17:20],inst[20:25],inst[25:32],counter)
    elif type=="S":
        execute_S_type(inst[0:7],inst[7:12],inst[12:17],inst[17:20],inst[20:25],inst[25:32])
    elif type=="B":
        imm=inst[0]+inst[24]+inst[1:7]+inst[20:24]
        execute_B_type(imm,inst[7:12],inst[12:17],inst[17:20],counter)
    elif type=="U":
        execute_U_type(inst[0:20],inst[20:25],inst[25:32],counter)
    elif type=="J":
        imm=inst[0]+inst[12:20]+inst[11]+inst[1:11]
        execute_J_type(imm,inst[20:25],counter)
    
f=open("output.txt","w")

y=0
while y<x:
    f.write(format(y,'032b'))
    f.write(" ")
    execute(PC[y],y)
    for i in registers:
        f.write(format(registers[i],'032b'))
        f.write(" ")
    y+=4
    f.write("\n")

for address, value in memory.items():
    decimal_value = int(str(value), 2)  # Convert binary value to decimal
    f.write(f"0x{address:08x}:0b{decimal_value:032b}\n")  # Write decimal value to output file

f.close()