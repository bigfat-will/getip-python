from flask import Flask
from flask import request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get():
    ip = get_ip()
    return {"ip": ip}


@app.route('/region', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_with_ip():
    ip = request.args.get('ip')
    if ip is None:
        ip = get_ip()

    regions = region(ip)
    return {"ip": ip, "region": regions}


def get_ip():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    if ip is None:
        ip = request.environ.get("Proxy-Client-IP")
    if ip is None:
        ip = request.environ.get("WL-Proxy-Client-IP")
    if ip is None:
        ip = request.remote_addr
    return ip


def region(ip):
    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) Chrome/65.0.3325.181'}
    res = requests.get("https://ip.900cha.com/%s.html" % (ip), headers=ua)
    soup = BeautifulSoup(res.content.decode('utf-8'))
    list = soup.findAll('li', class_='list-item mt-2')
    regions = []
    for l in list:
        regions.append(l.text.split('->')[1].strip())
    return regions


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
