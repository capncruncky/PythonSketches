#!/usr/bin/env python

import sys

def usage():
    print("Usage:\nvalidateMAC [options] <MAC_ADDRESS> | <Valid_MAC_file> <Test_MAC_file>")
    print("Options:\n\t-c Convert <MAC_ADDRESS> to decimal|hexadecimal notation")

def cleanMAC(macAddress):
    if '.' or ':' in macAddress:
        if '.' in macAddress:
            macAddress = macAddress.replace('.','')
        elif ':' in macAddress:
            macAddress = macAddress.replace(':','')
    return macAddress

def convertMAC(macAddress):
    #macAddress is in decimal form...
    if '.' in macAddress:
        stripMAC = cleanMAC(macAddress)
        newMAC = ''
        charCount = 0
        for char in stripMAC:
            newMAC = newMAC + char
            charCount += 1
            if charCount == 2 and (len(newMAC) <= 16):
                newMAC = newMAC + ':'
                charCount = 0

    #macAddress is in hex form...
    elif ':' in macAddress:
        stripMAC = cleanMAC(macAddress)
        newMAC = ''
        charCount = 0
        for char in stripMAC:
            newMAC = newMAC + char
            charCount += 1
            if charCount == 4 and (len(newMAC) <= 13):
                newMAC = newMAC + '.'
                charCount = 0
    print(newMAC)
           
def compareMACs(file1, file2):    
    try:
        #open argument file
        file_01obj = open(file1, 'r')     #open 1st arg file
        file_02obj = open(file2, 'r')     #opne 2nd arg file    
    except IOError as err:
        print("Error: {0}".format(err))
        return 1

    #create dict for colored text
    #this uses ANSI escape sequences to color output in terminal
    #terminal must have these enabled
    class txtColors:
        VALID = '\033[92m'
        INVALID = '\033[91m'
        UNTESTED = '\033[94m'
        WHITE = '\033[00m'

    #create lists to store line entries
    f1 = []
    f2 = []
    validMACs = []
    invalidMACs = []

    #iterate through file_01.txt entry lines
    for line in file_01obj:
        newLine = cleanMAC(line.rstrip())
        if newLine == 1:
            return 1
        else:
            #add each line into a list and strip newline char
            f1.append(newLine)

    for line in file_02obj:
        newLine = cleanMAC(line.rstrip())
        if newLine == 1:
            return 1
        else:
            #add each line into a list and strip newline char
            f2.append(newLine)

    file_01obj.close()
    file_02obj.close()

    #Sort/Compare
    for addr in f2:
        if addr in f1:
            validMACs.append(addr)
        else:
            invalidMACs.append(addr)              
                
    #Display results
    print("\n" + txtColors.WHITE + "Valid MACs")           
    for item in validMACs:
        print(txtColors.VALID + item)
       
    print("\n" + txtColors.WHITE + "Rogue MACs")
    for item in invalidMACs:
        print(txtColors.INVALID + item)

    print("\n" + txtColors.WHITE + "Tested MACs")
    for item in f1:
        print(txtColors.UNTESTED + item + txtColors.WHITE)

def main():
    #validate argument count
    if len(sys.argv) < 3:
        usage()
        return 1

    elif len(sys.argv) == 3:
        if sys.argv[1][0] == '-':
            if sys.argv[1][1] == 'c':
                convertMAC(sys.argv[2])
                return 0
            else:
                print("Invalid argument")
                usage()
                return 1
        else:
            compareMACs(sys.argv[1], sys.argv[2])
    else:
        usage()
        return 1 

if __name__ == '__main__':
    main()
