import requests
import netifaces
from bs4 import BeautifulSoup

# 获取指定网卡的IP地址
interface_name = "eth0" # 替换为你的网卡名称
ip_address = netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]['addr']

# 构造请求参数
url = "https://www.whjyj.cn/lfradius/libs/portal/unify/portal.php/login/Ikuai8_login/"
payload = {
    "usrname": "*****",
    "passwd": "*****",
    "treaty": "on",
    "nasid": "1",
    "usrmac": "c6:bc:80:9d:07:f0",
    "usrip": ip_address,
    "basip": "http://1.0.0.0/webradius",
    "success": "https://www.whjyj.cn/lfradius/libs/portal/unify/portal.php/login/success/",
    "fail": "https://www.whjyj.cn/lfradius/libs/portal/unify/portal.php/login/fail/",
    "offline": "1",
    "portal_version": "",
    "portal_papchap": ""
}

# 发送第一次POST请求
response = requests.post(url, data=payload)

# 获取cookie
cookie = response.cookies.get_dict()

# 打印cookie
print("Cookie:", cookie)

# 使用 BeautifulSoup 解析响应内容，获取表单
soup = BeautifulSoup(response.text, 'html.parser')
form = soup.find('form')

# 构造表单参数
form_data = {}
for input_tag in form.find_all('input'):
    form_data[input_tag.get('name')] = input_tag.get('value')

# 发送第二次POST请求，并携带cookie
form_url = form.get('action')
response = requests.post(form_url, data=form_data, cookies=cookie)

# 打印响应内容
print(response.text)
