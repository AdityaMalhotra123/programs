import sys
if len(sys.argv) == 2:

    #declare variables

    k = int(sys.argv[1])

    #get user input
    plaintext = input("plaintext: ")
    print("ciphertext: ",end = '')
    #encrypt - iterate over each caracter in the string (plaintext)
    for i in range(len(plaintext)):

        #uppercase letters
        if plaintext[i].isupper():

            #shift plaintext by key
            ciphertext = ((ord(plaintext[i]) - 65) + k) % 26
            #print encrypted message character by character
            ciphertext = ciphertext + 65
            print((chr(ciphertext)),end = '')

        #lowercase letters
        elif plaintext[i].islower():

            #shift plaintext by key
            ciphertext = ((ord(plaintext[i]) - 97) + k) % 26;
            #print encrypted message character by character
            ciphertext = ciphertext + 97
            print((chr(ciphertext)),end = '')

        #if non-alphabet
        elif plaintext[i].isalpha() != True:
            #print without shifting/changing
            print(plaintext[i],end = '')



    #newline to make the output more neat and presentable
    print("");


#if there are more or less than two cammand line arguments
else:

    #error message
    print("Usage: ./caesar k")


