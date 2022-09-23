def read_and_write(file):
    myFile1 = open(file, "r")
    
    myLst = ["\",", "\"\t", ",\"", "\t\"", "true,", "true\t", "false,", "false\t"]    
    
    data = myFile1.read().replace(myLst[0], myLst[1]) \
                            .replace(myLst[2], myLst[3]) \
                            .replace(myLst[4], myLst[5]) \
                            .replace(myLst[6], myLst[7])
    
    myFile2 = open("ds.tsv", "w")
    myFile2.write(data)
    myFile1.close()
    myFile2.close()

if __name__ == '__main__':
    read_and_write("ds.csv")