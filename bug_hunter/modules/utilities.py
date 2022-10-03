import builtins
from random import randint


results = "./results"
useragents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254",
    "Mozilla/5.0 (Linux; Android 12; SM-X906C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36"
    ]


#   CUSTOM PRINT
def print(text):
    builtins.print("*" * 10 + " {} ".format(text) + "*" * 10)


#   GET RANDOM USER AGENT
def get_useragent():
    return useragents[randint(0, len(useragents) - 1)]

#   GET UNIQUE SUBDOMAINS
def get_unique(iterable):
    return list(set(iterable))


#   WRITE A FILE
def write_file(filename, data_list):
    with open(filename, "wt") as file:
        for item in data_list:
            file.writelines("{}\n".format(item))
        file.close()


#   READ A FILE
def read_file(filename):
    with open(filename, "rt") as file:
        data_list = file.readlines()
        file.close()
    return data_list


#   RETURNS URL FORM A GIVEN PROTOCOL, DOMAIN, PORT
def get_url(proto, subd, port=80):
    if ((proto == "https") and (port == 80)):
        port = 443
    url = "{}://{}:{}".format(proto, subd, port)
    print(url)
    return url