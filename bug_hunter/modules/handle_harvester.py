import os
import threading
from time import sleep
from utilities import print

total_subdomains = list()

def launch(domain):
    global total_subdomains

    #   THE HARVESTER SOURCES
    sources=["anubis", "baidu", "bing", "binaryedge", "bingapi", "bufferoverun", "censys", "certspotter", "crtsh", "dnsdumpster", "duckduckgo", "fullhunt", "github-code", "google",
            "hackertarget", "hunter", "intelx", "linkedin", "linkedin_links", "n45ht", "omnisint", "otx", "pentesttools", "projectdiscovery", "qwant", "rapiddns", "rocketreach",
            "securityTrails", "spyse", "sublist3r", "threatcrowd", "threatminer", "trello", "twitter", "urlscan", "virustotal", "yahoo", "zoomeye"]

    sources_ammount = len(sources)    

    threads_list = list()

    #   THE HARVESTER
    print("LAUNCHING theHarvester")
    print("CHECKING IN {} SOURCES".format(sources_ammount))
    for i in range(0, sources_ammount):
        thread = threading.Thread(target=thread_the_harvester, args=(domain, sources[i]))  
        thread.start()   
        threads_list.append(thread)
        sleep(0.2)
    print("*" * 20)

    for thread in threads_list:
        thread.join()

    return total_subdomains


#   THREAD START FOR THE HARVESTER
def thread_the_harvester(domain, source):
    global total_subdomains

    resp_parsed = exec_harvester_cmd(domain, source)

    subdomains = resp_parsed_scrap(resp_parsed, domain)
    
    total_subdomains += subdomains


#   GETTING RESPONSES FROM THE HARVESTER THREAD AND PARSING IT
def resp_parsed_scrap(resp_parsed, domain):
    subdomains = list()

    for subd in resp_parsed:
        if ("{}:".format(domain) in subd):
            clear_subdomain = subd.split(":")[0]
            subdomains.append(clear_subdomain)

    return subdomains


#   ACTUALLY LAUNCHES THE HARVESTER CMD
def exec_harvester_cmd(domain, source):
    cmd_harvest = "theHarvester -d {} -b {} -s -v -n".format(domain, source) 
    resp = os.popen(cmd_harvest).read()
    resp_parsed = resp.split("\n")
    return resp_parsed
