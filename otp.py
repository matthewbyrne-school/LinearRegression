''' OTP Encryption '''
# Author: Matthew Byrne
# Date: 7/10/19

# One Time Pad Enc/Dec Module (Vernam Cipher)

# Imports
import random

# key generation
def eightBitKeyGen():
    num = random.randint(0, 255)
    key =  '{0:08b}'.format(num)

    return key

# Encryption using key and binary input
def encryptString(k, m):
    c = ""
    for i in range(len(m)-1):
        c += str(int(m[i]) ^ int(k[i]))

    return c