# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 14:41:14 2022

@author: medici
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 12:08:54 2022

@author: medici
"""


# Version 4



# variable underscore naming convention
# file Camel Naming Convention

import re
import os
from collections import Counter

os.chdir("D:\\06")
#import pandas as pd

# str.isdigit
path = "pong/Pong.hack" # storage
# if @ ( is coupled for a symbol, the it is a symbol, give a value for it based on (
# if it is not coupled, give value from 0

# Symbol dictionary
array_symbol = []
array_symbolJmp = []
array_symbolJmpOri = []



all_lines = open("pong/Pong.asm")

incre = 0
for line in all_lines:
    line_str = str(line)
    line_len = len(line_str)
    if(line_str[:2]=='//' or line_len<=1):
        print("skip due to // and empty line")
    #elif(line_str[0]=='@' or line_str[0]=='('):
    else:
        line_str_strp = line_str.replace("\n","").strip()
        line_str_strp_c = line_str_strp.find("//")
        if(line_str_strp_c>0):
            array_symbol.append(line_str_strp[:line_str_strp_c].strip())
            print(line_str_strp)
        else:
            array_symbol.append(line_str_strp.strip())
        #array_symbol.append(line_str_strp_c)
        # add_target.write('0'+binary_ins+'\n')

#Transform jump label to @ label

for line in array_symbol:
    line_str = str(line)
    line_len = len(line_str)
    if(line_str[:2]=='//' or line_len<=1):
        print("skip due to // and empty line")
    #elif(line_str[0]=='@' or line_str[0]=='('):
    elif(line_str[0]=='('):
        array_symbolJmp.append(line_str.replace("\n","").strip().replace("(","@").replace(")",""))
        array_symbolJmpOri.append(line_str.replace("\n","").strip())
        # add_target.write('0'+binary_ins+'\n')
#Get code list

all_lines_exclude = []
all_lines_exclude_ori = []



for line in array_symbol:
    line_str = str(line).strip()
    line_len = len(line_str)
    if(line_str[:2]=='//' or line_len<=1):
        print("skip due to // and empty line")
    else:
        all_lines_exclude_ori.append(line.replace("\n","").strip())

for line in array_symbol:
    line_str = str(line).strip()
    line_len = len(line_str)
    if(line_str[0]=='@' or line_str[0]=='('):
        all_lines_exclude.append(line.replace("\n","").strip())
    else:
        print("skip due to // and empty line")

# Get the index of jump symbol 15 in [13,15]
symbol_collection = {'syntax':[],'row_n':[]}
symbol_collection_t = {'syntax':[],'row_n':[]}

for inx, line in enumerate(all_lines_exclude_ori):
    line_str = str(line)
    line_len = len(line_str)
    i = len(symbol_collection_t['syntax'])
    if(line_str[:2]=='//' or line_len<=1):
        print("skip due to // and empty line")
    #elif(line_str[0]=='@' or line_str[0]=='('):
    elif(line_str[0]=='('):
        
        symbol_collection['syntax'].append(line_str.replace("\n","").strip())
        symbol_collection['row_n'].append((inx-i))
        
        symbol_collection_t['syntax'].append(line_str.replace("\n","").strip().replace("(","@").replace(")",""))
        symbol_collection_t['row_n'].append((inx-i))

#symbol_collection remove duplicate
all_lines_exdist = []

for line in all_lines_exclude:
    if((line in all_lines_exdist)):
        print("skip")
    else:
        all_lines_exdist.append(line)


# Incremental assignment

inc = 16

incR = 0

symbol_codeN = {'syntax':[],'row_n':[]}

for inx,line in enumerate(all_lines_exdist):
    if((line in symbol_collection['syntax']) or (line in array_symbolJmp) or (str.isdigit(str(line[1:])))):
        print("skip")
    elif(line=='@SCREEN'):
        symbol_codeN['syntax'].append(line)
        symbol_codeN['row_n'].append(16384)
    elif(line[:3]=='@SP'):
        symbol_codeN['syntax'].append(line)
        symbol_codeN['row_n'].append(0)
    elif(line[:4]=='@LCL'):
        symbol_codeN['syntax'].append(line)
        symbol_codeN['row_n'].append(1)
    elif(line[:4]=='@ARG'):
        symbol_codeN['syntax'].append(line)
        symbol_codeN['row_n'].append(2)
    elif(line[:5]=='@THIS'):
        symbol_codeN['syntax'].append(line)
        symbol_codeN['row_n'].append(3)
    elif(line[:5]=='@THAT'):
        symbol_codeN['syntax'].append(line)
        symbol_codeN['row_n'].append(4)
    elif(line[:4]=='@KBD'):
        symbol_codeN['syntax'].append(line)
        symbol_codeN['row_n'].append(24576)
        
    elif(line[:2]=='@R'):
        symbol_codeN['syntax'].append(line)
        symbol_codeN['row_n'].append(line[2:])
    else:
        symbol_codeN['syntax'].append(line)
        while(inc in symbol_codeN['row_n']):
            inc = inc + 1
        symbol_codeN['row_n'].append(inc)
        inc = inc + 1



# View
import pandas as pd

codeN_table = pd.DataFrame(symbol_codeN)
codeJ_table = pd.DataFrame(symbol_collection)
codeJt_table = pd.DataFrame(symbol_collection_t)

code_merged = pd.merge(codeN_table, codeJt_table, how='outer')

# for inx,line in zip(code_merged['row_n'],code_merged['syntax']):
#     print(str(inx) +" "+ str(line))


add_target = open(path,"w")

for line in array_symbol:
    line_str = str(line).strip().replace("\n","")
    line_len = len(line_str)
    if(line_str[:2]=='//' or line_len<=1):
        print("skip due to // and empty line")
    elif(line_str[0]=='@' or line_str[0]=='('):# this could be the only part that will be affected
        if(str.isdigit(line_str[1:])):
            binary_ins = bin(int(line[1:])).replace("0b","").zfill(15)
            print(binary_ins)
            add_target.write('0'+binary_ins+'\n')
        elif(line_str[0]=='('):
            print("skip")
        else:
            print("symbol line monitor" + str(line_str))
            for inx_sub,line_sub in zip(code_merged['row_n'],code_merged['syntax']):
                inx_sub = str(inx_sub)
                if(line_str==line_sub):
                    # binary_ins = bin(int(inx_sub).replace("0b","").zfill(15)
                    # add_target.write('0'+binary_ins+'\n')
                    # print("")
                    binary_ins = bin(int(inx_sub)).replace("0b","").zfill(15)
                    add_target.write('0'+binary_ins+'\n')
                    print("executed once")
                    break
            print("symbol line monitor number" + str(binary_ins))
    else:
        
        print("c instroction")
        
        eq_sign = line_str.find("=")
        comma_sign = line_str.find(";")
        
        if(";" in line_str):
            if("=" in line_str):
                # Has jump, has assignment
                print("print Has jump, has assignment")  
                #jmp = 000
                eq_left = line_str[:eq_sign]
                eq_right = line_str[eq_sign+1:comma_sign]
                
                comma_right = line_str[comma_sign+1:].replace("\n","")
                
                # Jump part
                if(comma_right=="JGT"):
                    jmp = "001"
                elif(comma_right=="JEQ"):
                    jmp = "010"
                elif(comma_right=="JGE"):
                    jmp = "011"                      
                elif(comma_right=="JLT"):
                    jmp = "100"   
                elif(comma_right=="JNE"):
                    jmp = "101"   
                elif(comma_right=="JLE"):
                    jmp = "110"   
                elif(comma_right=="JMP"):
                    jmp = "111"
                else:
                    jmp = "000"
                
                # Computing part
                if(eq_right=="D"):
                    cmp = "0001100"
                elif(eq_right=="A"):
                    cmp = "0110000"
                elif(eq_right=="M"):
                    cmp = "1110000"
                elif(eq_right=="0"):
                    cmp = "0101010"
                elif(eq_right=="1"):
                    cmp = "0111111"
                elif(eq_right=="-1"):
                    cmp = "0111010"
                
                elif(eq_right=="!D"):
                    cmp = "0001101"
                elif(eq_right=="!A"):
                    cmp = "0110001"
                elif(eq_right=="-D"):
                    cmp = "0001111"  
                elif(eq_right=="-A"):
                    cmp = "0110011" 
                elif(eq_right=="D+1"):
                    cmp = "0011111" 
                elif(eq_right=="A+1"):
                    cmp = "0110111" 
                elif(eq_right=="D-1"):
                    cmp = "0001110" 
                elif(eq_right=="A-1"):
                    cmp = "0110010" 
                elif(eq_right=="D+A"):
                    cmp = "0000010" 
                elif(eq_right=="D-A"):
                    cmp = "0010011" 
                elif(eq_right=="A-D"):
                    cmp = "0000111" 
                elif(eq_right=="D&A"):
                    cmp = "0000000" 
                elif(eq_right=="D|A"):
                    cmp = "0010101" 

                elif(eq_right=="!M"):
                    cmp = "1110001"
                elif(eq_right=="-M"):
                    cmp = "1110011" 
                elif(eq_right=="M+1"):
                    cmp = "1110111" 
                elif(eq_right=="M-1"):
                    cmp = "1110010" 
                elif(eq_right=="D+M"):
                    cmp = "1000010" 
                elif(eq_right=="D-M"):
                    cmp = "1010011" 
                elif(eq_right=="M-D"):
                    cmp = "1000111" 
                elif(eq_right=="D&M"):
                    cmp = "1000000" 
                elif(eq_right=="D|M"):
                    cmp = "1010101" 
                else:
                    print("print")                    
                    
                # Destination
                if(eq_left=="M"):
                    dest = "001"
                elif(eq_left=="D"):
                    dest = "010"
                elif(eq_left=="MD"):
                    dest = "011"           
                elif(eq_left=="A"):
                    dest = "100"  
                elif(eq_left=="AM"):
                    dest = "101"
                elif(eq_left=="AD"):
                    dest = "110" 
                elif(eq_left=="AMD"):
                    dest = "111"
                else:
                    dest = "000"
            else:
                # Has jump, no assignment
                print("print Has jump, no assignment")  
                comma_left = line_str[:comma_sign]
                
                comma_right = line_str[comma_sign+1:].replace("\n","")
                # Jump part
                if(comma_right=="JGT"):
                    jmp = "001"
                elif(comma_right=="JEQ"):
                    jmp = "010"
                elif(comma_right=="JGE"):
                    jmp = "011"                      
                elif(comma_right=="JLT"):
                    jmp = "100"   
                elif(comma_right=="JNE"):
                    jmp = "101"   
                elif(comma_right=="JLE"):
                    jmp = "110"   
                elif(comma_right=="JMP"):
                    jmp = "111"
                else:
                    jmp = "000"
                
                
                dest = "000"
                if(comma_left=="D"):
                    cmp = "0001100"
                elif(comma_left=="A"):
                    cmp = "0110000"
                elif(comma_left=="M"):
                    cmp = "1110000"
                elif(comma_left=="0"):
                    cmp = "0101010"
                else:
                    print("print Has jump, no assignment")            
        else:
            
            if("=" in line_str):
                # No jump, has assignment
                print("print No jump, has assignment")     
                jmp = "000"
                eq_left = line_str[:eq_sign]
                eq_right = line_str[eq_sign+1:].replace("\n","")
                
                # Computing part
                if(eq_right=="D"):
                    cmp = "0001100"
                elif(eq_right=="A"):
                    cmp = "0110000"
                elif(eq_right=="M"):
                    cmp = "1110000"
                elif(eq_right=="0"):
                    cmp = "0101010"
                elif(eq_right=="1"):
                    cmp = "0111111"
                elif(eq_right=="-1"):
                    cmp = "0111010"
                
                elif(eq_right=="!D"):
                    cmp = "0001101"
                elif(eq_right=="!A"):
                    cmp = "0110001"
                elif(eq_right=="-D"):
                    cmp = "0001111"  
                elif(eq_right=="-A"):
                    cmp = "0110011" 
                elif(eq_right=="D+1"):
                    cmp = "0011111" 
                elif(eq_right=="A+1"):
                    cmp = "0110111" 
                elif(eq_right=="D-1"):
                    cmp = "0001110" 
                elif(eq_right=="A-1"):
                    cmp = "0110010" 
                elif(eq_right=="D+A"):
                    cmp = "0000010" 
                elif(eq_right=="D-A"):
                    cmp = "0010011" 
                elif(eq_right=="A-D"):
                    cmp = "0000111" 
                elif(eq_right=="D&A"):
                    cmp = "0000000" 
                elif(eq_right=="D|A"):
                    cmp = "0010101" 

                elif(eq_right=="!M"):
                    cmp = "1110001"
                elif(eq_right=="-M"):
                    cmp = "1110011" 
                elif(eq_right=="M+1"):
                    cmp = "1110111" 
                elif(eq_right=="M-1"):
                    cmp = "1110010" 
                elif(eq_right=="D+M"):
                    cmp = "1000010" 
                elif(eq_right=="D-M"):
                    cmp = "1010011" 
                elif(eq_right=="M-D"):
                    cmp = "1000111" 
                elif(eq_right=="D&M"):
                    cmp = "1000000" 
                elif(eq_right=="D|M"):
                    cmp = "1010101" 
                else:
                    print("print No jump, has assignment")                    
                    
                # Destination
                if(eq_left=="M"):
                    dest = "001"
                elif(eq_left=="D"):
                    dest = "010"
                elif(eq_left=="MD"):
                    dest = "011"           
                elif(eq_left=="A"):
                    dest = "100"  
                elif(eq_left=="AM"):
                    dest = "101"
                elif(eq_left=="AD"):
                    dest = "110" 
                elif(eq_left=="AMD"):
                    dest = "111"
                else:
                    dest = "000"
            else:
                # No jump, no assignment
                print("No jump, no assignment")
                jmp = "000"
                dest = "000"
                if(line_str=="D"):
                    cmp = "0001100"
                elif(line_str=="A"):
                    cmp = "0110000"
                elif(line_str=="M"):
                    cmp = "1110000"
                else:
                    print("No jump, no assignment")
            
        binary_ins = str("111") + str(cmp) + str(dest) + str(jmp)
        add_target.write( binary_ins +'\n')
        #add_target.write('1'+dest+'\n')
add_target.close()
