import sys

def my_alphabet():
    key1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    key2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    value = range(26)
    a = dict(zip(key1, value))
    A = dict(zip(key2, value))
    return a, A

def return_alphabet(c):
    alph, ALPH = my_alphabet()
    if ord(c) >= 65 and ord(c) <= 90:
        return ALPH
    if ord(c) >= 97 and ord(c) <= 122:
        return alph
    return None

def if_in_alphabet(c):
    if (ord(c) >= 65 and ord(c) <= 90) or \
       (ord(c) >= 97 and ord(c) <= 122):
       return True
    return False

def in_ascii(text):
    if all(ord(char) < 128 for char in text) == False:
        raise ValueError("The script does not support your language yet")

def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key
    
def sum_in_al(letter, tab):
    alphabet = return_alphabet(letter)
    num = alphabet[letter]
    for i in range(tab):
        if num == 25:
            num = -1
        num += 1
    return get_key(alphabet, num)

def sub_in_al(letter, tab):
    alphabet = return_alphabet(letter)
    num = alphabet[letter]
    for i in range(tab):
        if num == 0:
            num = 26
        num -= 1
    return get_key(alphabet, num)

def encoding(elem, tab):
    encoded_str = ""
    for i in range(len(elem[2])):
        if if_in_alphabet(elem[2][i]):
            encoded_str += sum_in_al(elem[2][i], tab)
        else:
            encoded_str += elem[2][i]
    print(encoded_str)

def decoding(elem, tab):
    encoded_str = ""
    for i in range(len(elem[2])):
        if if_in_alphabet(elem[2][i]):
            encoded_str += sub_in_al(elem[2][i], tab)
        else:
            encoded_str += elem[2][i]
    print(encoded_str)

def caesar():
    if len(sys.argv) != 4:
        raise ValueError('Incorrect number of arguments')
    in_ascii(sys.argv[2])
    encoded_str = ""
    tab = int(sys.argv[3])
    if (sys.argv[1] == 'encode'):
        encoding(sys.argv, tab)
    elif (sys.argv[1] == 'decode'):
        decoding(sys.argv, tab)
    else:
        raise ValueError('Unknown action')

if __name__ == '__main__':
    caesar()