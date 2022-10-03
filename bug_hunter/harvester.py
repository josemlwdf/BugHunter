import sys
import os
import threading
from modules import \
    handle_vhosts, http_probe, handle_harvester, handle_sublister, \
    utilities, handle_wafwoof, handle_eyewitness, handle_cewl



#   GLOBALS
total_subdomains = list()

os.makedirs(utilities.results)

def main():
    #   MOTD    ************************************************************************************
    #   GLOBALS
    global total_subdomains

    #   CHECK ARGS    
    try:
        if (len(sys.argv) > 0):
            domain = sys.argv[1].replace("*.", "").strip()
        else:
            domain = input().strip()
    except:
        print("INCORECT NUMBER OF PARAMS")
        exit()

    #   SCANS   ************************************************************************************

    print("*" * 20)
    print("SCANNING {}".format(domain))
    print("*" * 20)

    dns_scans(domain)

    total = len(total_subdomains)

    #   END OF DNS SCANS    *****************************************************************************

    print("DONE. {} TOTAL SUBDOMAINS FOUND".format(total))
    print("*" * 20)

    #   HTTP PROBE RESOLVE URLs    *****************************************************************************

    print("URL SUBDOMAINS ENUMERATION")
    print("*" * 20)

    #   GET VALID URLS & BRUTEFORCE SUBDOMAINS OVER HTTP
    print("LAUNCHING HTTP PROBE")
    print("*" * 20)
    total_subdomains = http_probe.launch(total_subdomains)

    thread_subprograms_list = list()

    #   CHECK URLs BEHIND WAF
    print("CHECKING WAF")
    print("*" * 20)
    print("LAUNCHING WAFW00F")
    print("*" * 20)
    thread = threading.Thread(target=handle_wafwoof.launch, args=(total_subdomains, ))
    thread.start()
    thread_subprograms_list.append(thread)

    print("CHECKING VHOSTS")
    print("*" * 20)
    thread = threading.Thread(target=handle_vhosts.launch, args=(total_subdomains, ))
    thread.start()
    thread_subprograms_list.append(thread)

    print("TAKING SCREENSHOTS")
    print("*" * 20)
    thread = threading.Thread(target=handle_eyewitness.launch, args=(total_subdomains))
    thread.start()
    thread_subprograms_list.append(thread)

    print("CREATING WORDLISTS")
    print("*" * 20)
    thread = threading.Thread(target=handle_cewl.launch, args=(total_subdomains))
    thread.start()
    thread_subprograms_list.append(thread)

    join_threads(thread_subprograms_list)


def join_threads(threads_list):
    for thread in threads_list:
        thread.join()


#   LAUNCHES DNS_SCANNERS
def dns_scans(domain):
    global total_subdomains
    threads_list = list()

    print("DNS ENUMERATION")
    print("*" * 20)

    thread = threading.Thread(target=launch_harvester, args=(domain, ))  
    thread.start()   
    threads_list.append(thread)

    thread = threading.Thread(target=launch_sublister, args=(domain, ))  
    thread.start()   
    threads_list.append(thread)

    for thread in threads_list:
        thread.join()

    #   GET UNIQUE SBDOMAINS
    filename=domain

    total_subdomains.append(domain)

    total_subdomains = utilities.get_unique(total_subdomains)

    utilities.write_file("{}/dns_{}".format(utilities.results, filename), total_subdomains)


#   LAUNCH theHarvester
def launch_harvester(domain):
    global total_subdomains
    total_subdomains += handle_harvester.launch(domain)


#   LAUNCH sublsit3r
def launch_sublister(domain):
    global total_subdomains
    total_subdomains += handle_sublister.launch(domain)


""" if (__name__ == "__main__"):
    main() """

dns_scans("usbr.gov")