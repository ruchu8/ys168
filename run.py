import os
import requests

def login_to_server(url, params, headers):
    try:
        response = requests.post(url, data=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        if "ERR" in response.text or "管理密码不正确" in response.text:
            return False, "登录失败，密码错误"
        else:
            return True, "登录成功"
    except requests.exceptions.RequestException as e:
        return False, f"请求出错: {str(e)}"

# 登录信息和URL
url = 'http://ht.ys168.com/login.aspx'
params = {
    'cz': 'Dl',
    'yhm': 'cqbd',
    'glmm': 'qq496789'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}

# 执行登录
login_success, login_message = login_to_server(url, params, headers)

# 打印登录结果
print(login_message)

# 获取登录时间和IP
from datetime import datetime, timezone, timedelta
beijing_timezone = timezone(timedelta(hours=8))
time = datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')
response = requests.get('https://myip.ipip.net/json')
data = response.json()
loginip = data['data']['ip']

# 获取GitHub Actions的环境变量
push = os.getenv('PUSH')

# 定义推送邮件的方法
def mail_push(url, content):
    data = {
        "body": content,
        "email": os.getenv('MAIL')
    }
    try:
        response = requests.post(url, json=data)
        response_data = json.loads(response.text)
        if response_data['code'] == 200:
            print("推送成功")
        else:
            print(f"推送失败，错误代码：{response_data['code']}")
    except requests.exceptions.RequestException as e:
        print(f"连接邮箱服务器失败: {str(e)}")
    except json.JSONDecodeError:
        print("响应内容不是有效的JSON格式")

# 定义推送Telegram的方法
def telegram_push(message):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
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
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"发送消息到Telegram失败: {response.text}")
        else:
            print("推送成功")
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {str(e)}")

# 准备推送内容
content = f"登录时间: {time}\n登录IP: {loginip}\n{login_message}"

# 根据环境变量选择推送方式
if push == "mail":
    mail_push('https://zzzwb.us.kg/test', content)
elif push == "telegram":
    telegram_push(content)
else:
    print("推送失败，推送参数设置错误")
