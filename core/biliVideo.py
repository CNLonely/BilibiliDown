import requests

def get_play_info(bvid,aid,cid,title,cookies=None):
    if not bvid:
        raise ValueError("无法提取 BVID")
    # 请求的 headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.bilibili.com/',
    }
   
    # 构造请求链接
    url = (
        f"https://api.bilibili.com/x/player/wbi/playurl?qn=120&fnver=0&fnval=4048&fourk=1&voice_balance=1&gaia_source=pre-load&isGaiaAvoided=true&"
        f"avid={aid}&bvid={bvid}&cid={cid}&"
    )

    # 请求的 headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    # 发送请求
    response = requests.get(url, headers=headers, cookies=cookies)

    # 处理响应
    if response.status_code == 200:
        data = response.json()

        video_data = data['data']['dash']['video']
        audio_data = data['data']['dash']['audio'][0]

        video_info = []

        for i in range(len(video_data)):
            video_info.append({
                'title': title,
                'baseURL': video_data[i]['baseUrl'],
                'width': video_data[i]['width'],
                'height': video_data[i]['height'],
                'frameRate': video_data[i]['frameRate'],
                'audioURL': audio_data['baseUrl']
            })
        

        return video_info  # 返回播放信息数据
    else:
        raise Exception(f"请求失败，状态码：{response.status_code}")

