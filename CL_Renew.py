import requests
from bs4 import BeautifulSoup
import sys

CL_Username = ''
CL_Password = ''

header_login = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
           "Host": "accounts.craigslist.org",
           "Origin": "https://accounts.craigslist.org",
           "Referer": "https://accounts.craigslist.org/login"}

data = {"step": "confirmation",
        "inputEmailHandle": CL_Username,
        "inputPassword": CL_Password}

s = requests.Session()

r = s.post('https://accounts.craigslist.org/login',
           headers=header_login, data=data)

r = s.get("https://accounts.craigslist.org/login/home")

soup = BeautifulSoup(r.content, features="html.parser")

header_renew = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
           "Host": "post.craigslist.org",
           "Origin": "https://accounts.craigslist.org",
           "Referer": "https://accounts.craigslist.org/login"}

forms = soup.find_all('form', {'class': 'manage'})
for form in forms:
    if form.find('input',{'name': 'action'}).get('value') == 'renew':
        title = form.parent.parent.find_next_sibling('td').find('a').text.strip().split('\n')[0]
        url = form['action']
        crypt = form.find('input',{'name': 'crypt'})['value']
        payload = {'action': 'renew', 'crypt': crypt, 'go': 'renew'}
        s.post(url, headers=header_renew, data=payload)
        print("Renewed: %s" % title)
