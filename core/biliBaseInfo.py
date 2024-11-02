import requests
import re
import json

def get_bili_url_baseInfo(bili_url,cookies=None):    # 提取 BVID
    bvid = None
    if 'bilibili.com' in bili_url:
        match = re.search(r'BV[0-9A-Za-z]+', bili_url)
        if match:
            bvid = match.group(0)
    else:
        bvid = bili_url

    # 请求的 headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.bilibili.com/',
    }

    # 通过 BVID 获取 AID 和 CID
    view_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    view_response = requests.get(view_url, cookies=cookies, headers=headers)


    if view_response.status_code == 200:
        view_data = view_response.json()
        bili_info = {
            'title': view_data['data']['title'],
            'pic': view_data['data']['pic'],
            'bvid': view_data['data']['bvid'],
            'aid': view_data['data']['aid'],
            'cid': view_data['data']['cid'],
            'time': view_data['data']['pubdate'],
            'desc': view_data['data']['desc']
        }

    #判断是否获取成功
    if not bili_info:
        print("Failed to retrieve video information.")
        return None

    return bili_info

def get_bili_cookies():
    try:
        # 从 user.json 中读取 cookies
        with open('./data/user.json', 'r', encoding='utf-8') as f:
            user_data = json.load(f)

        # 提取 cookies
        if user_data and "url_params" in user_data:
        
            url_params = user_data['url_params']
            cookies = {
                "DedeUserID": url_params["DedeUserID"],
                "DedeUserID__ckMd5": url_params["DedeUserID__ckMd5"],
               "SESSDATA": url_params["SESSDATA"],
                "bili_jct": url_params["bili_jct"],
            }
            return cookies
        else:
            print("No cookies found in user.json")
            return None
    except FileNotFoundError:
        print("用户尚未登录或cookies文件失效")
        return None



    