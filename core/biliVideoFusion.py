import requests
import subprocess
import os

def download_and_merge_video(title, base_url, audio_url):
    # 创建所需目录
    os.makedirs('./data/cache/video', exist_ok=True)
    os.makedirs('./data/video', exist_ok=True)

    video_path = './data/cache/video/video.m4s'
    audio_path = './data/cache/video/audio.m4s'
    output_path = f'./data/video/{title}_output.mp4'

    # 下载视频
    video_response = requests.get(base_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.bilibili.com/',
    })
    with open(video_path, 'wb') as video_file:
        video_file.write(video_response.content)

    # 下载音频
    audio_response = requests.get(audio_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.bilibili.com/',
    })
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(audio_response.content)

    # 转换视频文件格式
    subprocess.run(['ffmpeg', '-i', video_path, '-c', 'copy', './data/cache/video/video.mp4'])
    subprocess.run(['ffmpeg', '-i', audio_path, '-c', 'copy', './data/cache/video/audio.mp4'])

    # 合并视频和音频
    subprocess.run(['ffmpeg', '-i', './data/cache/video/video.mp4', '-i', './data/cache/video/audio.mp4',
                    '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_path])

    # 删除临时文件
    os.remove(video_path)
    os.remove(audio_path)
    os.remove('./data/cache/video/video.mp4')
    os.remove('./data/cache/video/audio.mp4')

    print("视频和音频已成功合并为:", output_path)

if __name__ == '__main__':
    # 使用示例
    title = "视频标题"
    base_url = 'https://xy61x147x214x139xy.mcdn.bilivideo.cn:4483/upgcxcode/...'
    audio_url = 'https://xy118x184x254x101xy.mcdn.bilivideo.cn:8082/v1/resource/...'
    
    download_and_merge_video(title, base_url, audio_url)
