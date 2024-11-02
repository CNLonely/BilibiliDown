import requests
import time
import qrcode
import json
from urllib.parse import urlparse, parse_qs

def save_qr_image(content, filename="./data/cache/bilibili_qr.png"):
    """生成二维码图像并保存"""
    img = qrcode.make(content)
    img.save(filename)
    print(f"二维码已保存到 {filename}")

def generate_qrcode():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    }
    
    # 请求生成二维码的URL和qrcode_key
    response = session.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main_web&go_url=&web_location=333.1228", headers=headers)

    # 打印响应内容，方便调试
    print("响应内容:", response.text)

    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return None

    try:
        data = response.json()
    except ValueError as e:
        print("解析JSON失败:", e)
        return None

    if data["code"] != 0:
        print("获取二维码失败:", data["message"])
        return None

    # 获取URL和qrcode_key
    qrcode_url = data["data"]["url"]
    qrcode_key = data["data"]["qrcode_key"]
    print(f"二维码URL: {qrcode_url}")
    print(f"二维码key: {qrcode_key}")

    # 生成二维码图像
    save_qr_image(qrcode_url)

    return qrcode_key

def poll_qrcode_status(qrcode_key):
    """轮询二维码状态"""
    session = requests.Session()
    url = f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}&source=main_web&web_location=333.1228"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    }

    while True:
        try:
            response = session.get(url, headers=headers, timeout=10)  # 添加超时参数
        except requests.exceptions.Timeout:
            print("请求超时，请检查网络连接。")
            break
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            break

        # 打印响应内容，方便调试
        print("轮询状态响应内容:", response.text)

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            break

        try:
            data = response.json()
        except ValueError as e:
            print("解析JSON失败:", e)
            break

        # 检查二维码的状态
        if data["code"] == 0:
            if data["data"]["code"] == 0:
                print("登录成功！")
                print("登录成功后的所有参数:", data)
                # 保存登录成功后的参数到 user.json
                save_login_data(data["data"])
                break
            elif data["data"]["code"] == 86101:
                print("未扫码，请继续等待...")
            elif data["data"]["code"] == 86038:
                print("二维码已过期，请重新生成。")
                break
            elif data["data"]["code"] == 86090:
                print("二维码已扫码未确认")
            else:
                print("未知状态，等待扫码...")
        else:
            print("轮询失败:", data["message"])

        time.sleep(2)  # 增加轮询间隔

def save_login_data(data):
    """保存登录数据到 user.json"""
    filename = "./data/user.json"

    # 从 URL 中提取参数
    url_data = data.get("url", "")
    url_params = parse_qs(urlparse(url_data).query)

    # 将数据分割成多条
    save_data = {
        "url": url_data,
        "refresh_token": data.get("refresh_token", ""),
        "timestamp": data.get("timestamp", 0),
        "code": data.get("code", 0),
        "message": data.get("message", ""),
        "url_params": {key: value[0] for key, value in url_params.items()},  # 取出每个参数的第一个值
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)

    print(f"登录数据已保存到 {filename}")

def check_login(cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    }
    url = 'https://api.bilibili.com/x/space/myinfo'

    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        if response.json().get('code') == -101:
            return False
        elif response.json().get('code') == 0:
            return True
        else:
            return False




def test():
    qrcode_key = generate_qrcode()
    if qrcode_key:
        print("请扫描生成的二维码进行登录...")
        poll_qrcode_status(qrcode_key)


if __name__ == "__main__":
    test()
