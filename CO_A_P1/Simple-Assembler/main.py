#***************************************************GROUP-A50*******************************************************************#
#MEMBERS:- ARYAN, 2022109
#          AYUSH KUMAR, 2022124
#          KARTIKEYA MALIK, 2022243
#          AKSHAT WADHERA, 2022057
#***************************************************CO GROUP PROJECT - ASSEMBLER************************************************#

#   File import through text file then using sys to take it as standard input
import sys
output=''
ky=''
for kx in sys.stdin:
    ky+=kx

f = open("input.txt", "w")
f.write(ky)
f.close()

f = open("input.txt", "r")
data = f.read()
with open('input.txt') as f:  # here input.txt is an input file with assembly code 
    code = f.read().splitlines()

#*********************************************Now the main code**************************************************************************#

operations = {"add":["00000","A"],"sub":["00001","A"],"mov1":["00010","B"],"mov2":["00011","C"],"ld":["00100","D"],"st":["00101","D"],"mul":["00110","A"],
    "div":["00111","C"],"rs":["01000","B"],"ls":["01001","B"],"xor":["01010","A"],"or":["01011","A"],"and":["01100","A"],"not":["01101","C"],
   "cmp":["01110","C"],"jmp":["01111","E"],"jlt":["11100","E"],"jgt":["11101","E"],"je":["11111","E"],"hlt":["11010","F"],"mov":"to avoid terminator",
   "addf": ["10000", "A"],"subf": ["10001", "A"],"movf": ["10010", "B"],"inc":["10011", "B"],"dec":["10100", "B"],"jz":["10101", "E"],"jnz":["10111", "E"],"jne":["11000", "E"]
}
RegAddress = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
varr=[] # for storing variables
terminator=False # terminates wholes function and shows error
reg = [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6","FLAGS"]
labels=["hlt"]  # for storing labels

#Error Handling

#Type A
def type_A(value,terminator):
    if len(value) != 4:
        print("line no", curline, "wrong syntax used for", value[0], "instruction")
        terminator = True
        return terminator

    i = 1
    while i < len(value):
        if value[i] == "FLAGS":
            print("line no", curline, "invalid use of flags")
            terminator = True
        elif value[i] not in reg:
            print("line no", curline, f"({value[i]}) is an invalid register name")
            terminator = True
        i += 1
        return terminator

#Type B
def type_B(value,terminator):
    if len(value) != 3:
        print("line no", curline, "wrong syntax used for", value[0], "instruction")
        terminator = True
        return terminator

    if value[1] == "FLAGS":
        print("line no", curline, "invalid use of flags")
        terminator = True
    elif value[1] not in reg:
        print("line no", curline, f"({value[1]}) is an invalid register name")
        terminator = True

    a = value[2]
    if a[0] != "$":
        print("line no", curline, "use of", a[0], "is invalid")
        terminator = True
    else:
        try:
            n = int(a[1:])
            assert 0 <= n <= 255, f"{a} is not in range [0, 255]"
        except AssertionError as e:
            print(f"line no {curline}: {a} {e}")
            terminator = True
        except:
            print(f"line no {curline}: invalid immediate value")
            terminator = True
    return terminator
        
#Type C
def type_C(value,terminator):
    if(len(value)!=3):
        print("line no" , curline , " wrong syntax used for type C instruction",sep=' ' )
        terminator=True
        return terminator

    if(value[1]=="FLAGS"):
        print("line no" , curline, " invalid use of flags ",sep=' ')
        terminator=True

    elif(value[1] not in reg):
        print("line no" , curline ,'(',value[1],')', "is invalid register name ",sep=' ')
        terminator=True

    if(value[0]=="mov2" and value[2] not in reg):
        print("line no" , curline , " invalid register or flag name ",sep=' ')
        terminator=True

    elif value[0]!="mov2" and value[2] not in reg:
        print("line no",curline,"invalid register name",sep=' ')
        terminator=True
    return terminator
        
#Type D
def type_D(value,terminator):
    if len(value) != 3:
        print("line no", curline, "wrong syntax used for", value[0], "instruction")
        terminator = True
        return terminator

    if value[2] in labels:
        print("line no", curline, "labels cannot be used in place of varr")
        terminator = True
    elif value[2] not in varr:
        print("line no", curline, f"({value[2]}) is an undefined variable")
        terminator = True
    return terminator

#Type E
def type_E(value,terminator):
    if len(value) != 2:
        print("line no", curline, "wrong syntax used for", value[0], "instruction")
        terminator = True
        return terminator

    if value[1] in varr:
        print("line no", curline, "varr cannot be used in place of labels")
        terminator = True
    elif value[1] not in labels:
        print("line no", curline, f"({value[1]}) is an undefined label")
        terminator = True
    return terminator
        
#Type F
def type_F(value,terminator):
    if curline != len(code):
        print("line no", curline, "hlt must be at the end")
        terminator = True
    elif len(value) != 1:
        print("line no", curline, "wrong syntax used for", value[0], "instruction")
        terminator = True
        return terminator
        
#Helper function to handle varaibles
def handle_variables(value,terminator):
    global flag
    if value[0] != "var":
        flag = 1

    if value[0] == "var" and len(value) != 2:
        print("line no", curline, "invalid syntax")
        terminator = True
        return

    if value[0] == "var":
        if flag == 1:
            print("line no", curline, "variable not declared in the beginning of code")
            terminator = True
        if value[1] in varr:
            print("line no", curline, "multiple declaration of variable", value[1])
            terminator = True
        elif value[1] not in varr:
            varr.append(value[1])
        return terminator

#Helper function to handle labels
def handle_labels(value,terminator):
    if value[0][-1] == ":":
        label_name = value[0][:-1]
        if label_name in labels:
            print("line no", curline, "multiple definitions of label", f"({value[0]})")
            terminator = True
        else:
            labels.append(label_name)
    return terminator
       
#Helper function to handle Halt
def handle_lhlt(value,terminator):
    if len(value) == 2:
        if value[1] != "hlt":
            print("line no", curline + 1, "no hlt instruction at the end")
            terminator = True
    elif value[0] != "hlt":
        print("line no", curline + 1, "no hlt instruction at the end")
        terminator = True
    return terminator

#Error handling for each and every cases of variables
curline = 0
flag = 0

for line in code:
    curline += 1
    if not line:
        continue
    value = line.split()
    terminator=handle_variables(value,terminator)
       
#Error handling for each and every cases of labels
curline = 0

for line in code:
    curline += 1
    if not line:
        continue
    value = line.split()
    terminator=handle_labels(value,terminator)

#Handling every case for Base Code
curline = 0

for line in code:
    curline += 1
    if not line:
        continue

    value = line.split()

    if curline == len(code):
        terminator=handle_lhlt(value,terminator)

    if value[0] == "var":
        continue

    if value[0][:-1] in labels:
        value.pop(0)

    if not value:
        print("line no", curline, "invalid definition of labels")
        terminator = True
        continue

    if value[0] not in operations.keys():
        print("line no", curline, f"({value[0]}) is an invalid instruction name")
        terminator = True
        continue

    if value[0] == "mov" and len(value) >= 2:
        c = value[2][0]
        if c == "$":
            value[0] = "mov1"
        else:
            value[0] = "mov2"

    if operations[value[0]][1] == "A":
        terminator=type_A(value,terminator)

    elif operations[value[0]][1] == "C":
        terminator=type_C(value,terminator)

    elif operations[value[0]][1] == "B":
        terminator=type_B(value,terminator)

    elif operations[value[0]][1] == "D":
        terminator=type_D(value,terminator)

    elif operations[value[0]][1] == "E":
        terminator=type_E(value,terminator)

    elif operations[value[0]][1] == "F":
        terminator=type_F(value,terminator)

    else:
        print("line no", curline, "invalid syntax")
        terminator = True

#code to print into binary

labels={}
varr={}

t=1
address=-1

if(terminator==True):
    sys.exit()

#code to store the address of each variable in the dictionary
for line in code:
    if not line:
        continue
    value = line.split()

    if value[0] in operations.keys():
        address += 1

    if value[0] == "hlt":
        labels[value[0] + ":"] = address

    if value[0][-1] == ":":
        address += 1
        labels[value[0]] = address

#code to store the address of each variable in the labels
for line in code:
    if not line:
        continue
    value = line.split()
    if value[0] == "var" and len(value) == 2:
        varr[value[1]] = t + address
        t += 1

#Main code to convert assembly into binary
for line in code:
    if not line:
        continue

    value = line.split()
    if len(value) > 1 and value[0] in labels and value[1] in operations.keys():
        value.pop(0)

    if value[0] in operations.keys():
        if value[0] == "mov":
            if value[2][0] == "$":
                value[0] = "mov1"
            else:
                value[0] = "mov2"

        if operations[value[0]][1] == "B":
            if value[0] == "movf":
                a = value[1]
                b = value[2][1:]
                s = operations[value[0]][0] +  RegAddress[a] + bin(int(b))[2:].zfill(8)
            else:
                a = value[1]
                b = value[2][1:]
                b1 = bin(int(b))[2:]
                s = operations[value[0]][0] + "0" + RegAddress[a] + (7 - len(b1)) * "0" + b1

        elif operations[value[0]][1] == "A":
            a = value[1]
            b = value[2]
            c = value[3]
            s = operations[value[0]][0] + "00" + RegAddress[a] + RegAddress[b] + RegAddress[c]

        elif operations[value[0]][1] == "C":
            a = value[1]
            b = value[2]
            s = operations[value[0]][0] + "00000" + RegAddress[a] + RegAddress[b]

        elif operations[value[0]][1] == "D":
            a = value[1]
            b = bin(varr[value[2]])[2:]
            s = operations[value[0]][0] + "0" + RegAddress[a] + (7 - len(b)) * "0" + b

        elif operations[value[0]][1] == "E":
            a = value[1]
            b = bin(labels[a + ":"])[2:]
            s = operations[value[0]][0] + "000" + (8 - len(b)) * "0" + b

        elif operations[value[0]][1] == "F":
            s = operations[value[0]][0] + "00000000000"

        output += s+'\n'
sys.stdout.write(output)