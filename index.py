import requests
from bs4 import BeautifulSoup
import threading
from pprint import pprint
import time

BASE_URL = "https://streamingcommunity"

# ::TIME OF EXECUTION USING OPTIMIZED VERSION: 42.972890853881836
# ::TIME OF EXECUTION USING ICANN LIST VERSION: 52.974562883377075

# WebVersion using url
def get_urls():
    tld_base = []
    r = requests.get("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
    for x in str(r.text).split("\n"):
        if x.strip() or "#" or "-" not in x:
            tld_base.append(BASE_URL + "." + x.strip().lower())
    return tld_base

# optimization using file without brand tld (TOCHECK)
""" def get_urls():
    tld_base = []
    for x in open("tld_list.txt","r"):
        tld_base.append(BASE_URL + "." + str(x).strip().lower())
    return tld_base """

# V1 of function to check streamingcommunity string presence
def check_1(url, results):
    try:
        r = requests.get(url, timeout=5)  # Imposta il timeout a 10 secondi
        if r.status_code == 200:
            bs = BeautifulSoup(r.content, features="html.parser")
            for x in bs.findAll("meta", {"name":"author"}):
                if "StreamingCommunity" in x.get("content"):
                    results.append(url)
                    break
    except:
        pass

urls = get_urls()
results = []

threads = []

#start time execution
inizio = time.time()

for url in urls:
    thread = threading.Thread(target=check_1, args=(url, results))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("\n================================")
for result in results:
    print(result)

#end time execution
fine = time.time()
tempo_di_esecuzione = fine - inizio
print(tempo_di_esecuzione)