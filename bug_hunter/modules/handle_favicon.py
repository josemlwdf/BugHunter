import sys, os
from hashlib import md5
import requests
from re import findall
from time import sleep

headers={"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}

def get_favicon_url(url):
    if ('http://' not in url) and ('https://' not in url):
        url = 'http://' + url
    print('[*] Scanning ' + url + '...')
    print('[*] Looking for favicon URL...')
    resp = requests.get(url,  headers=headers, allow_redirects=True)

    count = 0
    sleep_time = 1
    max_retries = 50
    while True:
        if (resp) or (count == max_retries):
            break
        sleep(sleep_time)
        count += 1

    if (not resp):
        print('[*] The site is not answering')
        exit(1)
    resp = resp.text.split()
    pattern = r'href=\".*?favicon.*?\"'
    for line in resp:
        match = findall(pattern, line)
        if match:
            break
    if (match):
        match = match[0].split('"')[1]
        proto = host = url.split('/')[0] + '//'
        host = url.split('/')[2]
        if ('https://' not in match) and ('http://' not in match):
            match = match.replace('//', '/')
            if (match[0] == '/'):
                arg_one = match.split('/')[1]
            else:
                arg_one = match.split('/')[0]
            if ('.' not in arg_one):                
                match = proto + host + match
            elif ('.' in arg_one):
                if (match[0] == '/'):
                    match = match[1:]
                match = proto + match
        print('[*] Found URL: ', match)
        return match
    else:
        if ('https://' not in url):
            if ('http://' in url):
                url = url.replace('http://', 'https://')
                fav_url = get_favicon_url(url)
                if (fav_url):
                    return fav_url
        print('[*] Favicon URL Not Found')
        exit(1) 


def get_favicon(url): 
    print('[*] Getting favicon hash from ' + url + '...')
    resp = requests.get(url,  headers=headers, allow_redirects=True)
    if (not resp):
        print('[*] We could not get the favicon, sorry')
        exit(1)
    _hash = md5(resp.content).hexdigest()
    return _hash


def owasp_search(_hash):
    url = 'https://wiki.owasp.org/index.php?search=' + _hash + '&title=Special%3ASearch&go=Go'
    print('[*] Searching ' + _hash + ' in OWASP Database...')
    resp = requests.get(url,  headers=headers, allow_redirects=True)
    if (not resp):
        print('[*] The site of OWASP is not responding')
        exit(1)
    pattern = r'<span class=\'searchmatch\'>.*</span>:.*\n'
    match = findall(pattern, resp.text)
    if (match):
        match = str(match).split(':')[1]
        print('[*] Match Found...')
    else:
        print('[*] Framework Not Found')
    return match


def main():
    usr_input = ''
    if (len(sys.argv) > 1):
        usr_input = sys.argv[1]
    else:
        print('USAGE: ' + sys.argv[0] + ' http://www.exampleurl.com')
        exit(1)
    fav_url = get_favicon_url(usr_input)
    _hash = get_favicon(fav_url)
    result = owasp_search(_hash)
    if (result): 
        print('[*] ', result)


if (__name__ == '__main__'):
    main()