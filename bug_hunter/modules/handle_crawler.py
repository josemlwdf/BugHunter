import requests
import re
import threading
from time import sleep
import os
from utilities import *


protocols = ["http", "https"]
unwanted_extensions = ["jpg", "ico", "png", "jpeg", "js", "css", "gif", "pdf", "mp3", "mp4", "flv"]

scrapped_urls = list()
pending_urls = list()


def launch(valid_urls):
	global pending_urls
	pending_urls = valid_urls

	thread = threading.Thread(target=crawl_launch, args=("",))
	thread.start()
	thread.join()

	for url in scrapped_urls:
		builtins.print(url)
	print(len(scrapped_urls))


def crawl_launch(nullarg):
	global pending_urls
	global scrapped_urls
	
	count = 0
	thread_list = list()

	while len(pending_urls) > 0:      
		url = pending_urls[0]  
		pending_urls.remove(url)

		if (url in scrapped_urls):
			continue
		
		scrapped_urls.append(url)

		print("starting thread for: " + url)

		thread = threading.Thread(target=thread_crawl, args=(url, url.split("/")[2], ))
		thread.start()
		count += 1
		thread_list.append(thread)

		if (count >= 5):
			sleep(1)
			join_threads(thread_list)
			count = 0
			thread_list.clear()
	
	join_threads(thread_list)


def thread_crawl(url, original_site):
	headers = {
            'User-Agent': get_useragent(),
        } 
	try:
		resp = requests.get(url=url, headers=headers)

		if ("20" in str(resp.status_code)):
			cmd_echo_save = "echo {} >> {}/{}/SITE_DATA".format(resp.text, results, original_site)
			os.popen(cmd_echo_save)
			get_urls(resp, original_site)

		if (("20" in str(resp.status_code)) or ("30" in str(resp.status_code))):			
			cmd_echo_save = "echo {} >> {}/{}/SITE_URLS".format(url, results, original_site)
			os.popen(cmd_echo_save)	

		print("response from: " + url + " is: " + resp.status_code)
	except:
		return


def get_urls(page_data, original_site):
	global pending_urls
	url_data = page_data.replace('"', '"\n"')
	local_urls = list()

	last_found_potocol = ""
	
	#	GET URLs
	for protocol in protocols:
		raw_urls = re.findall('"({}://.*?)["|#|\?]'.format(protocol), url_data)
		for url in raw_urls:
			if ((original_site in url) and (url.split(".")[-1] not in unwanted_extensions)):
				local_urls.append(url)
				last_found_potocol = protocol
				
	#	GET URIs
	raw_uri = re.findall('href="(?!http)(/.*?)["|#|\?]', page_data)
	url = ""
	for uri in raw_uri:
		url = "{}://{}{}".format(last_found_potocol, original_site, uri)
		if (url.split(".")[-1] not in unwanted_extensions):
			local_urls.append(url)

	pending_urls += get_unique(local_urls)
				

def get_comments(page_data):
	return


def join_threads(threads_list):
    for thread in threads_list:
        thread.join()


launch(["https://nuageo.fr"])