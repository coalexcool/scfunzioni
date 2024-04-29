import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
import time

# ::TIME OF EXECUTION: 47.55945014953613

BASE_URL = "https://streamingcommunity"

def get_urls():
    tld_base = []
    for x in open("tld_list.txt", "r"):
        tld_base.append(BASE_URL + "." + str(x).strip().lower())
    return tld_base

def check_1(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            bs = BeautifulSoup(r.content, features="html.parser")
            for x in bs.findAll("meta", {"name": "author"}):
                if "StreamingCommunity" in x.get("content"):
                    return url
    except:
        pass
    return None

urls = get_urls()

#start time execution
inizio = time.time()

results = []

with ThreadPoolExecutor(max_workers=800) as executor:  # Limita a 10 thread attivi contemporaneamente
    # Map restituisce un generatore di risultati, che possiamo convertire in una lista
    results = list(executor.map(check_1, urls))

results = [result for result in results if result is not None]  # Rimuove i risultati None

print("\n================================")
for result in results:
    print(result)

#end time execution
fine = time.time()
tempo_di_esecuzione = fine - inizio
print(tempo_di_esecuzione)
