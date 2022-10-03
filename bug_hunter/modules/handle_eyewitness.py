import threading
import requests
import json
from time import sleep
from utilities import results, get_useragent


total_subdomains = list()

def launch(valid_urls):

    for url in valid_urls:            
        thread = threading.Thread(target=thread_take_screenshot, args=(url, ))
        thread.start()
        thread.join()

        sleep(2)


#   THREAD FOR WAFF CHECK
def thread_take_screenshot(url) -> None:
    pikiw = "https://api.pikwy.com/?tkn=125&d=3000&u={}&fs=0&w=1280&h=1200&s=50&z=100&f=jpg&rt=jweb".format(url)
    headers = {
    'User-Agent': get_useragent(),
    }
    try:
        response = requests.get(pikiw, headers=headers)
        image_url = json.loads(response.text)["iurl"]
        image = requests.get(image_url)
        with open("{}/{}/{}.jpg".format(results, url, url), "wb") as file:
            file.write(image.content)
            file.close()
    except Exception as e:
        print(e)
    return