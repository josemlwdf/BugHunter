from  utilities import *
import threading
import requests
from string import printable
import os


#   GLOBALS
total_urls = list()
protocols = ["https", "http"]
dns_wordlist = "../resources/dns-Jhaddix.txt"
failed_subdomains = "failed_http_subdomains.txt"

#   HTTP PROBE
def launch(subdomains):
    global total_urls
    
    #   CHECK VALID URLs WITH MULTITHREAD
    check_valid_url(subdomains)

    print("{} VALID URLS FOUND".format(len(total_urls)))

    try:
        cmd_unique = "sort -u -o {} {}".format(failed_subdomains, failed_subdomains)
        os.popen(cmd_unique)
    except:
        ""

    print("START BRUTEFORCING URLS")
    print("*" * 20)

    #   BRUTEFORCE URLs WITH MULTI_THREAD
    brutef_subdomains(subdomains[0])

    total_urls = get_unique(total_urls)

    print("{} VALID URLS AFTER BRUTEFORCING".format(len(total_urls)))
    print("*" * 20)

    write_file("{}/valid_urls".format(results), total_urls)

    for url in total_urls:
        os.makedirs("{}/{}".format(results, url))

    return total_urls

#   ------------------------------------CHECKING URLs---------------------------------
#   CHECKS SUBDOMAIN FOR HTTP PROTOCOLS
def check_valid_url(subdomains) -> None:
    thread_list = list()

    count = 0

    for subdomain in subdomains:
        for protocol in protocols:
            thread = threading.Thread(target=check_url_thread, args=(protocol, subdomain.strip()))
            thread_list.append(thread)
            thread.start()
            count += 1

            if (count >= 100):
                count = 0
                join_threads(thread_list)
                thread_list.clear()
                
    join_threads(thread_list)


#   CHECKS URL IN A THREAD
def check_url_thread(protocol, subdomain):
        global total_urls

        url = get_url(protocol, subdomain)

        headers = {
            'User-Agent': get_useragent(),
        }

        try:
            resp = requests.get(url=url, headers=headers)

            if (("20" in str(resp.status_code)) or ("30" in str(resp.status_code))):
                total_urls.append(url)
            else:
                record_failures(subdomain)
        except Exception as e:
            if ("404" not in str(e)):
                record_failures(subdomain)


def record_failures(subdomain):
    os.popen("echo {} >> {}".format(subdomain, failed_subdomains))
    
#   ------------------------------------END CHECKING URLs---------------------------------

#   ------------------------------------BRUTEFORCING URLs---------------------------------
#   BRUTEFORCE HTTP SUBDOMAINS
def brutef_subdomains(subdomain):
    threads_list = list()
    
    #   BRUTEFORCE SUBDOMAINS
    domain_parts = subdomain.strip().split(".")
    domain = ".".join(domain_parts[1:])
    dns_list = read_file(dns_wordlist)

    count = 0

    for dns in dns_list:
        if (not all(char in printable for char in dns)):
            continue
        for protocol in protocols:
            count += 1
            subdomain = "{}.{}".format(dns.replace("\n", ""), domain)
            thread = threading.Thread(target=thread_brutef_http_dns, args=(protocol, subdomain, ))
            thread.start()
            threads_list.append(thread)

            if (count >= 100):
                join_threads(threads_list)
                count = 0
                threads_list.clear()

    join_threads(threads_list)


def join_threads(threads_list):
    for thread in threads_list:
        thread.join()


#   PART OF BRUTEFORCE MODULE
def thread_brutef_http_dns(protocol, subdomain):
    global total_urls
    
    url = get_url(protocol, subdomain)

    if (url in total_urls):
        return

    headers = {
            'User-Agent': get_useragent(),
        }

    try:
        resp = requests.get(url=url, headers=headers)

        if (("20" in str(resp.status_code)) or ("30" in str(resp.status_code))):
            total_urls.append(url)
    except Exception as e:
        return
#   ------------------------------------END BRUTEFORCING URLs---------------------------------
