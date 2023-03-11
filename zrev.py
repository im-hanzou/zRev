import requests
import re
import random
import urllib3
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def reverse_ip(ip):
    url = f"https://tools.webservertalk.com/?tool=reverseip&host={ip}"
    user_agent = UserAgent().random
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.content.decode("utf-8")
            domains = re.findall(r'<td class="text-left">(.+?)</td>', data)
            with open('reversed.txt', 'a') as f:
                for domain in domains:
                    f.write(domain + '\n')
            count = len(domains)
            print(ip + ': ' + str(count) + ' domains')
        else:
            print(ip + ': Failed to fetch data, Your IP blocked from API Host')
    except:
        print(ip + ': Failed to connect to the API, API Host down!')

def scan_ips(ips, threads):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        tasks = []
        for ip in ips:
            tasks.append(executor.submit(reverse_ip, ip.strip()))
        for task in tasks:
            task.result()

file_name = input("File list of IPs: ")

threads = int(input("Number threads to use: "))

with open(file_name, 'r') as f:
    ips = f.readlines()

scan_ips(ips, threads)

print("Reverse IP lookup done. Result saved to reversed.txt")
print("If you only got 1 domain, try to change your IP")
