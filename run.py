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
        
        # 仅新增这一行：打印登录接口返回的完整文本信息（核心需求）
        print("=== 登录接口返回完整信息 ===")
        print(response.text)

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
            
            print(content)  # 确保内容输出到控制台
            
            push = os.getenv('PUSH')
            if push == "telegram":
                telegram_push(content)
            else:
                print("没有设置有效的推送方式")

    except requests.exceptions.RequestException as e:
        print(f"请求登录页面时出错: {str(e)}")

def telegram_push(message):
    url_telegram = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    payload = {
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'text': message,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '问题反馈',
                        'url': 'https://t.me/CN_zzzwb'
                    }
                ]
            ]
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url_telegram, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"发送消息到Telegram失败: {response.text}")

# 调用登录函数
login_to_website()
