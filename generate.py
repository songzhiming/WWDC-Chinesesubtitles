import openai
import pysrt
import backoff  # for exponential backoff
import fire
import requests
from bs4 import BeautifulSoup
import subprocess

def getWWDCVideo(url,apikey):
    openai.api_key = apikey
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    # 查找视频URL
    video_tag = soup.find('video')
    video_url = None
    if video_tag:
        video_url = video_tag['src']
    title = soup.find('h1').text.strip()
    # 打印结果
    print('获取到视频URL:', video_url)
    print('获取到视频标题:', title)
    downloadWWDCUrl(video_url)
    getSrt("tmp.srt")
    srt_cmd = f'ffmpeg -i "new.srt" "new.vtt"'
    cmdFFmpeg(srt_cmd)
    output_file = title + ".mp4"
    print('output_file:', output_file)
    ffmpeg_cmd = f"ffmpeg -i tmp.mp4 -i tmp.aac -i new.vtt -map 0:v -map 1:a -acodec copy -vcodec copy -map 2 -c:s:0 mov_text -metadata:s:s:0 language=eng \"{output_file}\""
    cmdFFmpeg(ffmpeg_cmd)
    deleteCache()
    print("中英文字幕视频",output_file)
    
def deleteCache():
    files = ['tmp.mp4', 'tmp.aac', 'tmp.vtt', 'tmp.srt', 'new.srt', 'new.vtt']
    for file in files:
        try:
            subprocess.call(f'rm {file}', shell=True)
            print(f'Deleted file: {file}')
        except Exception as e:
            print(f'Error deleting file: {file}')
            print(f'Error message: {str(e)}')
    
    
def downloadWWDCUrl(url):
    videoM3u8 = url.replace("cmaf.m3u8", "cmaf/hvc/1080p_5800/hvc_1080p_5800.m3u8")
    audioM3u8 = url.replace("cmaf.m3u8", "cmaf/aac/lc_192/aac_lc_192.m3u8")
    vttM3u8 = url.replace("cmaf.m3u8", "subtitles/eng/prog_index.m3u8")
    print("视频M3U8:",videoM3u8)
    print("音频M3U8:", videoM3u8)
    print("字幕M3U8:", vttM3u8)
    print("下载视频ing")
    # 下载视频，音频，字幕
    videoM3u8_cmd = f'ffmpeg -i {videoM3u8} -c copy tmp.mp4'
    cmdFFmpeg(videoM3u8_cmd)
    audioM3u8_cmd = f'ffmpeg -i {audioM3u8} -c copy tmp.aac'
    cmdFFmpeg(audioM3u8_cmd)
    vttM3u8_cmd = f'ffmpeg -i {vttM3u8} -c copy tmp.vtt'
    cmdFFmpeg(vttM3u8_cmd)
    # 转换vtt  to  srt
    srt_cmd = f'ffmpeg -i tmp.vtt tmp.srt'
    cmdFFmpeg(srt_cmd)
    print("下载视频结束")

def cmdFFmpeg(cmd):
    subprocess.call(cmd, shell=True)

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def get_completion(prompt, model = "gpt-3.5-turbo"):
    message = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = message,
        temperature = 0
    )
    return response.choices[0].message["content"]

def translate(text):
    # 处理音乐
    if "♪" in text:
        return text
    else:
        prompt = f"""
                 将由三个反引号分隔的文本翻译成中文。
                 ```{text}```
                 """
        return get_completion(prompt)

def getSrt(path):
    srt = pysrt.open(path)
    print("Chatgpt翻译中-----")
    for element in srt.data:
        text = element.text
        translateText = translate(text).replace("```","")
        print(f'原文, {text}')
        print(f'翻译后, {translateText}')
        element.text = text + "\n" + translateText
    print("Chatgpt翻译结束-----")
    srt.save("new.srt")



if __name__ == '__main__':
    fire.Fire(getWWDCVideo)
