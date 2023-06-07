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
with open('input.txt') as f:  # here test_case1.txt is an input file with assembly code 
    code = f.read().splitlines()
output=""

operations = {"add":["00000","A"],"sub":["00001","A"],"mov1":["00010","B"],"mov2":["00011","C"],"ld":["00100","D"],"st":["00101","D"],"mul":["00110","A"],
    "div":["00111","C"],"rs":["01000","B"],"ls":["01001","B"],"xor":["01010","A"],"Or":["01011","A"],"And":["01100","A"],"not":["01101","C"],
   "cmp":["01110","C"],"jmp":["01111","E"],"jlt":["11100","E"],"jgt":["11101","E"],"je":["11111","E"],"hlt":["11010","F"],"mov":"to avoid terminater"
}
RegAddress = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
varr={} # for stroing variables
pc=0# program counter
registers = {"R0":0, "R1":0 , "R2":0, "R3":0 , "R4":0 , "R5":0 , "R6":0}
flag={"V":0,"L":0,"G":0,"E":0}
flagc={"V":0,"L":0,"G":0,"E":0}#copy for between updation
def add(r2,r3):
    global flag
    r1=r2+r3
    return r1
def sub(r2,r3):
    global flag
    if r3>r2:
        r1=0
        flag["V"]=1
    else:
        r1=r2-r3
    return r1
def mov1(value):
    r1=value
    return r1
def mov2(r2):
    r1=r2
    return r1
def ld (address,r1):
    if address in varr:
        r1=varr[address]
    else:
        print("no such address found")
def st(address,r1):
        if address in varr:
            varr[address]=r1
        else:
            varr[address]=r1
def mul(r2,r3):
    r1=r2*r3
    return r1
def div(r1,r2):
    global registers
    global flag
    if r2==0:
        flag["V"]=1
        registers["R1"]=0
        registers["R0"]=0
    else:
        registers["R0"]=r2//r1
        registers["R1"]=r2/r1-registers["R0"]
def rs(r1,value):
    re=r1>>value
    return re
def ls(r1,value):
    re=r1<<value
    return re
def xor(r2,r3):
    r1=r2^r3
    return r1
def Or(r2,r3):
    r1= r2|r3
    return r1
def And(r2,r3):
    r1=r2&r3
    return r1
def Not(r2):
    re=~r2
    return re
def cmp(r1,r2):
    global flag
    if r1==r2:
        flag["E"]=1
    elif r1>r2:
        flag["G"]=1
    elif r2>r1:
        flag["L"]=1
#custom functions to help
def findreg(r1):
    for i in RegAddress:
        if r1== RegAddress[i]:
            return i
def binaryToDecimal(binary):
    binary=int(binary)
    decimal = 0
    power = 1
    while binary>0:
        rem = binary%10
        binary = binary//10
        decimal += rem*power
        power = power*2
    return decimal
def printx():
    global output
    global pc
    global registers
    global flag
    maxx=65535
    r0=registers["R0"]
    r1=registers["R1"]
    r2=registers["R2"]
    r3=registers["R3"]
    r4=registers["R4"]
    r5=registers["R5"]
    r6=registers["R6"]
    l=[r0,r1,r2,r3,r4,r5,r6]
    dn={r0:"R0",r1:"R1",r2:"R2",r3:"R3",r4:"R4",r5:"R5",r6:"R6"}
    for i in l:   #for multiply and add overflow considering at one time only one will overflow at most
        if i>maxx:
            z=i
            registers[dn[i]]=0
            v=1
            flag["V"]=1
            break
    r0=registers["R0"]
    r1=registers["R1"]
    r2=registers["R2"]
    r3=registers["R3"]
    r4=registers["R4"]
    r5=registers["R5"]
    r6=registers["R6"]
    v=flag["V"]
    l=flag["L"]
    g=flag["G"]
    e=flag["E"]
    output +=(f"{'0'*(7-len(bin(pc)[2:]))}{bin(pc)[2:]}        {'0'*(16-len(bin(r0)[2:]))}{bin(r0)[2:]} {'0'*(16-len(bin(r1)[2:]))}{bin(r1)[2:]} {'0'*(16-len(bin(r2)[2:]))}{bin(r2)[2:]} {'0'*(16-len(bin(r3)[2:]))}{bin(r3)[2:]} {'0'*(16-len(bin(r4)[2:]))}{bin(r4)[2:]} {'0'*(16-len(bin(r5)[2:]))}{bin(r5)[2:]} {'0'*(16-len(bin(r6)[2:]))}{bin(r6)[2:]} {'0'*12}{v}{l}{g}{e}")+'\n' 
    #function to print

#main code starts here
while(pc<len(code)): #to move program counter to desired point in insturction execution
    i=code[pc]
    for j in operations:
        if operations[j][0]==i[:5]:
            if operations[j][1]=="A":
                opcode=i[:5]
                unused=i[5:7]
                reg1=i[7:10]
                reg2=i[10:13]
                reg3=i[13:]
                if reg1=="111" or reg2=='111' or reg3=="111":
                    printx()
                    pc+=1
                    continue
                if opcode=="00000":
                    registers[findreg(reg1)]=add(registers[findreg(reg2)],registers[findreg(reg3)])
                elif opcode=="00001":
                    registers[findreg(reg1)]=sub(registers[findreg(reg2)],registers[findreg(reg3)])
                elif opcode=="00110":
                    registers[findreg(reg1)]=mul(registers[findreg(reg2)],registers[findreg(reg3)])
                elif opcode=="01010":
                    registers[findreg(reg1)]=xor(registers[findreg(reg2)],registers[findreg(reg3)])
                elif opcode=="01011":
                    registers[findreg(reg1)]=Or(registers[findreg(reg2)],registers[findreg(reg3)])
                elif opcode=="01100":
                    registers[findreg(reg1)]=And(registers[findreg(reg2)],registers[findreg(reg3)])
            elif operations[j][1]=="B":
                opcode=i[:5]
                unused=i[5:6]
                reg1=i[6:9]
                imvalue=i[9:]
                if reg1=="111":
                    printx()
                    pc+=1
                    continue
                if opcode=="00010":
                    registers[findreg(reg1)]=mov1(binaryToDecimal(imvalue))
                elif opcode=="01000":
                    registers[findreg(reg1)]=rs(registers[findreg(reg1)],binaryToDecimal(imvalue))
                elif opcode=="01001":
                    registers[findreg(reg1)]=ls(registers[findreg(reg1)],binaryToDecimal(imvalue))
            elif operations[j][1]=="C":
                opcode=i[:5]
                unused=i[5:10]
                reg1=i[10:13]
                reg2=i[13:]
                if reg1=="111":
                    printx()
                    pc+=1
                    continue
                if reg2=="111":
                    x=str(flagc["V"])+str(flagc["L"])+str(flagc["G"])+str(flagc["E"])
                    y=binaryToDecimal(int(x))
                else:
                    y=registers[findreg(reg2)]
                if opcode=="00011":
                    registers[findreg(reg1)]=mov2(y)
                elif opcode=="00111":
                    div(registers[findreg(reg1)],y)
                elif opcode=="01101":
                    registers[findreg(reg1)]=Not(y)
                elif opcode=="01110":
                    cmp(registers[findreg(reg1)],y)
            elif operations[j][1]=="D":
                opcode=i[:5]
                unused=i[5:6]
                reg1=i[6:9]
                mem=i[9:]
                if reg1=="111":
                    printx()
                    pc+=1
                    continue
                if mem not in varr:
                    varr[mem]=None
                if opcode=="00100":
                    registers[findreg(reg1)]=varr[mem]
                elif opcode=="00101":
                    varr[mem]=registers[findreg(reg1)]
            elif operations[j][1]=="E":
                opcode=i[:5]
                unused=i[5:9]
                mem=i[9:]
                if opcode=="01111":
                    printx()
                    pc=binaryToDecimal(mem)
                    continue
                if opcode=="11100":
                    if flagc["L"]==1:
                        printx()
                        pc=binaryToDecimal(mem)
                        continue
                if opcode=="11101":
                    if flagc["G"]==1:
                        printx()
                        pc=binaryToDecimal(mem)
                        continue
                if opcode=="11111":
                    if flagc["E"]==1:
                        printx()
                        pc=binaryToDecimal(mem)
                        continue
            elif operations[j][1]=="F":
                printx()
                pc=999999
                break
            printx()
            pc+=1
    for t in flag:
       flagc[t]=flag[t]
    for j in flag:
        flag[j]=0
n=128 #remaining lines
for i in range(len(code)):
    output+=code[i]+'\n'
    n-=1
for i in varr:
    output+=f"{'0'*(16-len(bin(varr[i])[2:]))}{bin(varr[i])[2:]}"+'\n'
    n-=1
for i in range(n):
    output+=f"{'0'*16}"+'\n'

sys.stdout.write(output)
