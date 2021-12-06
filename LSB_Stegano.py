import cv2

def convert_to_decimal(test_str):
    res = ''.join(format(ord(i), '08b') for i in test_str)
    return res

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def decimalToBinary(n):
    return bin(n).replace("0b", "")
  
#Image size is 256*256
#Considering two pixels to be changed,
#Maximum change is 2*3*256*256
#However we will cap it at 9999 characters
#9999 characters requires 8*4 = 32 bits
#First 12 bits will be required to specify the length

def LSB_Steg():
    string = "Welcome to HackerShrine"
    message = convert_to_decimal(string)
    message_length = str(len(message))
    print("Original Message: ", string)
    
    if(len(message_length) > 4):
        print("String Length exceeded maximum value")
        return
    
    message_length = (4 - len(message_length))*"0" + message_length
    message = convert_to_decimal(str(message_length)) + message
    #Update Message Length
    message_length = len(message)
    #print(message)
    
    img = cv2.imread("Old_files/afghangirl.jpg")
    org_img = img.copy()
    count = 0

    for i in range(0, len(img)):
        if(count >= int(message_length)):
            break
        for j in range(0, len(img[0])):
            if(count >= int(message_length)):
                break
            for k in range(0, len(img[0][0])):
                bgr = img[i][j][k]
                img[i][j][k] = int((str(decimalToBinary(bgr))[:-2] + message[count:count+2]), 2)
                count = count + 2
                if(count >= int(message_length)):
                    break
                    
    cv2.imshow("Original Image", img)                
    cv2.imshow("Image with encoded message", img)
    cv2.moveWindow("Image with encoded message", 500, 180)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("--------Message Encoded-------")
    count = 0
    encoded_msg_len = ""
    encoded_msg = ""
    
    #Reverse
    
    #First, we need to get the length of the message
    #Hence we decode the first 32 bits first.
    
    for i in range(0, len(img)):
        if(count == 32):
            break
        for j in range(0, len(img[0])):
            if(count == 32):
                break
            for k in range(0, len(img[0][0])):
                bgr = img[i][j][k]
                encoded_msg_len = encoded_msg_len + str(decimalToBinary(bgr))[-2:]
                count = count + 2
                if(count == 32):
                    break
    encoded_msg_len = int(decode_binary_string(encoded_msg_len))
    encoded_msg_len = encoded_msg_len + 32
    
    count = 0
    
    for i in range(0, len(img)):
        if(count >= int(encoded_msg_len)):
            break
        for j in range(0, len(img[0])):
            if(count >= int(encoded_msg_len)):
                break
            for k in range(0, len(img[0][0])):
                bgr = img[i][j][k]
                encoded_msg = encoded_msg + str(decimalToBinary(bgr))[-2:]
                count = count + 2
                if(count >= int(encoded_msg_len)):
                    break
    print("Decoded Message: ", decode_binary_string(encoded_msg)[4:])
LSB_Steg()
