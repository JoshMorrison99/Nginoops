import sys
import requests
from urllib.parse import urlparse, parse_qs, urlencode
import urllib3
import re
import concurrent.futures

def banner():
    print('''
███    ██  ██████  ██ ███    ██  ██████   ██████  ██████  ███████
████   ██ ██       ██ ████   ██ ██    ██ ██    ██ ██   ██ ██
██ ██  ██ ██   ███ ██ ██ ██  ██ ██    ██ ██    ██ ██████  ███████
██  ██ ██ ██    ██ ██ ██  ██ ██ ██    ██ ██    ██ ██           ██
██   ████  ██████  ██ ██   ████  ██████   ██████  ██      ███████
Version 0.1                                            by Shelled\n''')

# Checks if the path with the slash (/) and without the slash returns the same result.
def off_by_slash_misconfiguration(url):
    url = url.strip('\n')
    url = urlparse(url)
    paths = (re.split('/', url.path[1:], 1))
    #print("[+] Debugger")
    #print(url)
    if(len(paths) > 1):
        #print(url)
        try:
            response1 = requests.get(url.scheme + '://' + url.netloc + '/' + paths[0] + '/' + paths[1])
            status1 = response1.status_code
            size1 = len(response1.content)

            response2 = requests.get(url.scheme + '://' + url.netloc + '/' + paths[0] + paths[1])
            status2 = response2.status_code
            size2 = len(response2.content)

            #print("    [" + str(status1) + "]" + "  " + "[" + str(size1) + "]" + "  " + url.scheme + '://' + url.netloc + '/' + paths[0] + '/' + paths[1])
            #print("    [" + str(status2) + "]" + "  " + "[" + str(size2) + "]" + "  " + url.scheme + '://' + url.netloc + '/' + paths[0] + paths[1])
        
            if((status1 == 200 and status2 == 200) and (size1 == size2)):
                print("[!] Off-By-Slash Misconfiguration")
                print(" -   [" + str(status1) + "]" + "  " + "[" + str(size1) + "]" + "  " + url.scheme + '://' + url.netloc + '/' + paths[0] + '/' + paths[1])
                print(" -   [" + str(status2) + "]" + "  " + "[" + str(size2) + "]" + "  " + url.scheme + '://' + url.netloc + '/' + paths[0] + paths[1])
        except:
            pass

def unsafe_variable_use(url):
    # Usage of $uri can lead to CRLF injection
    pass
    

banner()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
with concurrent.futures.ThreadPoolExecutor(50) as executor:
    executor.map(off_by_slash_misconfiguration, sys.stdin)
