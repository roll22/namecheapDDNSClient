#!/usr/bin/python3

import time
import requests
import socket


class Domain:
    def __init__(self, name, hosts, password):
        self.name = name
        self.hosts = hosts
        self.password = password


domains = []

domains.append(Domain(name='yourdomain1.com',
                      hosts=['@', 'yoursubdomain'],
                      password='password1'))
domains.append(Domain(name='domain2.org',
                      hosts=['@'],
                      password='password2'))

ip = ''
while ip == '':
    try:
        ip = socket.gethostbyname('yourdomain1.com')
        time.sleep(20)
    except socket.gaierror as e:
        print(e.args[1])

while True:
    url = "https://api.ipify.org/?format=json"
    timeout = 5
    # Alternate DDNS name provider alternative
    # ip2 = socket.gethostbyname('yourdnsprovider.com')
    try:
        request = requests.get(url, timeout=timeout)
        request = request.json()
        new_ip = request['ip']
        if new_ip != ip:
            for domain in domains:
                for host in domain.hosts:
                    req_url = 'https://dynamicdns.park-your-domain.com/update?' \
                              'host=' + host + '&' \
                                               'domain=' + domain.name + '&' \
                                                                         'password=' + domain.password + '&' \
                                                                                                         'ip=' + new_ip
                    request = requests.get(req_url, timeout=timeout)
                    print("Changed " + host + domain.name)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")

    time.sleep(120)
