import os
import requests
from datetime import datetime, timezone, timedelta

def login_to_website():
    url = "http://ht.ys168.com/login.aspx"
    username = os.getenv('LOGIN_USERNAME')
    password = os.getenv('LOGIN_PASSWORD')
    params = {
        "cz": "Dl",
        "yhm": username,
        "glmm": password
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常

        if "ERR 管理密码不正确" in response.text:
            print("登录失败，管理密码不正确")
        else:
            print("登录成功")
            beijing_timezone = timezone(timedelta(hours=8))
            time = datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')
            response_ip = requests.get('https://myip.ipip.net/json')
            data_ip = response_ip.json()
            loginip = data_ip['data']['ip']
            content = f"登录时间：{time}\n登录IP：{loginip}"
            
            push = os.getenv('PUSH')



# 调用登录函数
login_to_website()
