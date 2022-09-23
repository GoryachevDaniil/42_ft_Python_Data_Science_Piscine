#!/usr/local/bin/python3

def data_types():
    elems = (1, 'txt', 1.1, True, [1,'txt'], {'txt': 1}, (1, 'txt'), {1, 'txt'})
    myStr = "["
    for el in elems:
        myStr += str(type(el).__name__) + ', '
    myStr = myStr[:-2]
    myStr += "]"
    
    print(myStr)

if __name__ == '__main__':
    data_types()
