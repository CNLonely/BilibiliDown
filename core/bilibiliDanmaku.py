import requests
import re
from datetime import datetime

def get_danmaku(cid,cookies=None):
    # 请求的 headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.bilibili.com/',
    }

    # 请求弹幕
    url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
    response = requests.get(url, cookies=cookies, headers=headers)

    danmaku_data = response.content.decode('utf-8')

    # 解析弹幕
    return parse_danmaku(danmaku_data)


def parse_danmaku(danmaku_data):
    # 匹配每个弹幕数据
    pattern = r'<d p="([^"]+)">([^<]+)</d>'
    matches = re.findall(pattern, danmaku_data)

    # 存储解析后的弹幕
    danmaku_list = []

    for match in matches:
        properties = match[0].split(',')
        danmaku_info = {
            "time": float(properties[0]),      # 弹幕出现时间
            "timestamp": convert_timestamp(int(properties[4])),    # 发送时间戳
            "uid": properties[6],               # 用户ID
            "content": match[1]                # 弹幕内容
        }
        danmaku_list.append(danmaku_info)

    return danmaku_list

def convert_timestamp(timestamp):
    # 将时间戳转换为可读的时间格式
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')



