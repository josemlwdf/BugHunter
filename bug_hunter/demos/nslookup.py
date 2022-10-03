
import os
import threading
import sys

def main():
    threadlist = list()
    with open(sys.argv[1], "rt") as file:
        for line in file.readlines():
            thred = threading.Thread(target=nslookup, args=(line, ))
            thred.start()
            threadlist.append(thred)
        file.close()
    
    for thread in threadlist:
        thread.join()

def nslookup(line):
    resp = os.popen("nslookup -query=any -type=any {}".format(line)).read()
    print(resp)
        

main()
