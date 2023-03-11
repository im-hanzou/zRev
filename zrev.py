import requests
import re
from concurrent.futures import ThreadPoolExecutor

def reverse_ip(ip):
    url = f"https://tools.webservertalk.com/?tool=reverseip&host={ip}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"}
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
