import os
import threading
from utilities import print

total_subdomains = list()

def launch(domain):    
    keyword = "[-] Total Unique Subdomains Found"

    #   SUBLISTER
    print("LAUNCHING sublist3r")
    print("*" * 20)    
    
    thread = threading.Thread(target=thread_sublister, args=(domain, keyword))  
    thread.start()      
    thread.join()

    return total_subdomains


#   GETTING RESPONSES FROM sublist3r THREAD AND PARSING IT
def resp_parsed_scrap(resp_parsed, domain):
    subdomains = list()

    for subd in resp_parsed:
        if (domain in subd):
            subdomains.append(subd)

    return subdomains


def thread_sublister(domain, keyword):
    global total_subdomains
    resp = ""

    cmd_sublister = "sublist3r -d {} -n".format(domain)

    while keyword not in resp:        
        resp = os.popen(cmd_sublister).read()  
    
    total_subdomains += resp_parsed_scrap(resp.split(keyword)[1].split("\n"), domain)