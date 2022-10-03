import threading
import os
from utilities import results


#   WAFW00F
def launch(valid_urls):
    thread_list = list()

    count = 0

    for url in valid_urls:
        thread = threading.Thread(target=thread_waff_check, args=(url, ))
        thread.start()
        thread_list.append(thread)
        count += 1

        if (count >= 50):
            join_threads(thread_list)
            count = 0
            thread_list.clear()
    
    join_threads(thread_list)


#   THREAD FOR WAFF CHECK
def thread_waff_check(url):

    cmd_waff = "wafw00f {} -a -v".format(url)
    resp = os.popen(cmd_waff)

    if ("No WAF detected" not in resp):
        cmd_echo_save = "echo {} >> {}/{}/WAFF_PROTECTION".format(resp, results, url)
        os.popen(cmd_echo_save)
        return


def join_threads(threads_list):
    for thread in threads_list:
        thread.join()