import requests

def get_subtitles(bvid,aid,cid,cookies=None):
    # 请求的 headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.bilibili.com/',
    }

    # 构建播放器 API URL
    player_url = f"https://api.bilibili.com/x/player/wbi/v2?aid={aid}&cid={cid}"
    player_response = requests.get(player_url, cookies=cookies, headers=headers)

    if player_response.status_code == 200:
        player_data = player_response.json()
        # 提取字幕信息
        subtitles = player_data.get('data', {}).get('subtitle', {}).get('subtitles', [])
            
        # 创建返回的数据格式
        subtitle_info = {
            "subtitle_count": len(subtitles),
            "subtitles": []
        }

        for subtitle in subtitles:
            lan_doc = subtitle.get('lan_doc')
            subtitle_url = subtitle.get('subtitle_url')
            subtitle_info["subtitles"].append({
                "lan_doc": lan_doc,
                "subtitle_url": f"https:{subtitle_url}"
            })

        return subtitle_info  # 返回包含 BVID 和字幕信息的 JSON

    else:
        raise Exception(f"播放器请求失败，HTTP 状态码: {player_response.status_code}")

