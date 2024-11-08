from core.biliBaseInfo import *
from core.biliVideo import *
from core.bilibiliDanmaku import *
from core.biliVideoFusion import *
from core.biliSubtitle import *
from core.biliLogin import *

if __name__ == '__main__':
    cookies = get_bili_cookies() # 获取登录后的cookies
    if check_login(cookies) == False: # 检查是否登录成功
        print("请先登录哔哩哔哩") 
        qrcode_key = generate_qrcode() # 生成二维码 取qrcode_key
        if qrcode_key:
            print("请扫描生成的二维码进行登录...")
            poll_qrcode_status(qrcode_key) # 监听二维码状态
    else:
        print("已登录哔哩哔哩")
        bili_url = 'BV1bi421h79s' # 视频链接
        bili_baseinfo = get_bili_url_baseInfo(bili_url,cookies) # 获取视频基础信息 返回的结果包括了title,bvid,aid,cid,pic,time,desc
        title = bili_baseinfo['title']
        bvid = bili_baseinfo['bvid']
        aid = bili_baseinfo['aid']
        cid = bili_baseinfo['cid']
        video_info = get_play_info(bvid,aid,cid,title,cookies) # 获取视频下载地址 返回的结果包括了title,baseURL,audioURL,frameRate,width,height
        #download_and_merge_video(video_info[0]['title'],video_info[0]['baseURL'],video_info[0]['audioURL'])  # 下载视频并合并音频
        danmuku = get_danmaku(cid,cookies) # 获取弹幕信息 返回的结果包括了time,timestamp,text,uid
        subtitle = get_subtitles(bvid,aid,cid,cookies) # 获取字幕信息 返回的结果包括了subtitle_count,subtitle_list



