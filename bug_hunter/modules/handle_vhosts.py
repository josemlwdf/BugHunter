from time import sleep
import requests
import threading
from utilities import *
import os


original_urls = list()
dns_wordlist = "../resources/dns-Jhaddix.txt"
protocols = ["https", "http"]

def launch(valid_urls):
    thread_list = list()
    dns_list = read_file(dns_wordlist)
    count = 0

    domain = valid_urls[0].split("://")[1].split(".")
    domain = ".".join(domain[1:])

    for dns in dns_list:
        for protocol in protocols:
            host = get_url(protocol, "{}.{}".format(dns, domain))
            for url in valid_urls:            
                thread = threading.Thread(target=thread_check_vhosts, args=(url, host ))
                thread.start()
                thread_list.append(thread)
                count += 1

                if (count >= 2):
                    sleep(1)
                    join_threads(thread_list)
                    count = 0
                    thread_list.clear()
    
    join_threads(thread_list)


#   THREAD FOR WAFF CHECK
def thread_check_vhosts(url, host):
    headers = {"host" : host, 'User-Agent': get_useragent()}   
    try:
        resp = requests.get(url=url, headers=headers)

        if (("20" in str(resp.status_code)) or ("30" in str(resp.status_code))):
            cmd_echo_save = "echo {} >> {}/{}/VHOSTS".format(host, results, url)
            os.popen(cmd_echo_save)
    except:
        return


def join_threads(threads_list):
    for thread in threads_list:
        thread.join()