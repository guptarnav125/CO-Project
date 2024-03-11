def binary(decimal, num_bits):
    # Convert the absolute value of the decimal number to binary representation
    bin_abs = bin(abs(decimal))[2:]

    # Pad the binary representation with leading zeros to achieve the desired number of bits
    padded = bin_abs.zfill(num_bits)

    if decimal<0:
        # If the number is negative, perform two's complement
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in padded)
        # Add 1 to the inverted bits
        inverted_decimal = int(inverted_bits, 2) + 1
        # Get the binary representation of the inverted decimal
        twos_complement = bin(inverted_decimal)[2:].zfill(num_bits)
        return twos_complement
    else:
        # If the number is positive, return the binary representation
        return padded



f=open("input.txt","r")
list1=f.readlines()

R_type={"add":["0000000","000"],"sub":["0100000","000"],"sll":["0000000","001"],"slt":["0000000","010"],"sltu":["0000000","011"],"xor":["0000000","100"],"srl":["0000000","101"],"or":["0000000","110"],"and":["0000000","111"]}
B_type={"beq":"000","bne":"001","blt":"100","bge":"101","bltu":"110","bgeu":"111"}
S_type = {"sw":"010"}
I_type = {"lw":["010","0010011"],"addi":["000","0010011"],"sltiu":["011","0010011"],"jalr":["000","1100111"]}
U_type = {"lui":"0110111","auipc":"0010111"}
J_type = {"jal":"1101111"}
registers={"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011"}

x=12
for i in range(2,8):
    y=bin(x)[2:]
    if x<16:
        y="0"+y
    a=str(i)
    b="a"+a
    registers[b]=y
    x=x+1
x=18
for i in range(2,12):
    y=bin(x)[2:]
    a=str(i)
    b="s"+a
    registers[b]=y
    x=x+1
x=28
for i in range(3,7):
    y=bin(x)[2:]
    a=str(i)
    b="t"+a
    registers[b]=y
    x+=1

for i in list1:
    output=""
    list2=i.split()
    if list2[0] in R_type:
        list3=list2[1].split(",")
        output+=R_type[list2[0]][0]+registers[list3[2]]+registers[list3[1]]+R_type[list2[0]][1]+registers[list3[0]]+"0110011"
        print(output)
    elif list2[0] in B_type:
        list3=list2[1].split(",")
        x=int(list3[2])   
        y=binary(x,12)
        output+=y[0]+y[2:8]+registers[list3[1]]+registers[list3[0]]+B_type[list2[0]]+y[8:12]+y[1]+"1100011"
        print(output)
    elif list2[0] in J_type:
        list3=list2[1].split(",")
        x=binary(int(list3[1]),20)
        output+=x[0]+x[9:20]+x[8]+x[1:8]+registers[list3[0]]+J_type[list2[0]]
        print(output)
    elif list2[0] in U_type:
        list3 = list2[1].split(",")
        x = int(list3[1])
        y = binary(x, 20)
        output += y + registers[list3[0]] + U_type[list2[0]]
        print(output)
    elif list2[0] in I_type:
        if list2[0]=="lw":
            list3 = list2[1].split(",")
            imm_rs1 = list3[1].split("(")
            imm = int(imm_rs1[0])
            rs1 = imm_rs1[1][0:2]
            rd = list3[0]
            y = binary(imm, 12)
            output += y + registers[rs1] + I_type[list2[0]][0] + registers[rd] + "0010011"
            print(output)
        else:
            list3 = list2[1].split(",")
            if list2[0] == "jalr":
                imm_offset = list3[1].split("(")
                imm = int(imm_offset[0])
                rs1 = imm_offset[1][0]
            else:
                imm = int(list3[2])
                rs1 = list3[1]
            rd = list3[0]
            y = binary(imm, 12)
            output += y + registers[rs1] + I_type[list2[0]][0] + registers[rd] + I_type[list2[0]][1]
            print(output)
    elif list2[0] in S_type:
        list3 = list2[1].split(",")
        imm_rs1 = list3[1].split("(")
        imm = int(imm_rs1[0])
        rs1 = imm_rs1[1][0:2]
        rs2 = list3[0]
        y = binary(imm, 12)
        output += y[0:7] + registers[rs2] + registers[rs1] + S_type[list2[0]] + y[7:12] + "0100011"
        print(output)
f.close()
