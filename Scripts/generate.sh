## Session 10072 - Principles of spatial design
# 1.拉取音频，视频，字幕资源
ffmpeg -i https://devstreaming-cdn.apple.com/videos/wwdc/2023/10072/5/C43DFF91-F057-43E1-891F-41E6D5C01716/cmaf/hvc/1080p_5800/hvc_1080p_5800.m3u8 -c copy "Session - 10072 temp.mp4"
ffmpeg -i https://devstreaming-cdn.apple.com/videos/wwdc/2023/10072/5/C43DFF91-F057-43E1-891F-41E6D5C01716/cmaf/aac/lc_192/aac_lc_192.m3u8 -c copy "Session - 10072 temp.aac"
ffmpeg -i https://devstreaming-cdn.apple.com/videos/wwdc/2023/10072/5/C43DFF91-F057-43E1-891F-41E6D5C01716/subtitles/eng/prog_index.m3u8 -c copy "Session - 10072 temp.vtt"

# 2.vtt格式转srt格式
ffmpeg -i "Session - 10072 temp.vtt" "Session - 10072 temp.srt"

# 3.chatgpt翻译成中文
python3 translateSrt.py getSrt "Session - 10072 temp.srt" "TranslateSession - 10072 temp.srt"

# 4.srt转vtt格式
ffmpeg -i "TranslateSession - 10072 temp.srt" "TranslateSession - 10072 temp.vtt"

# 5.生成新的视频
ffmpeg -i "Session - 10072 temp.mp4" -i "Session - 10072 temp.aac" -i "TranslateSession - 10072 temp.vtt" -map 0:v -map 1:a -acodec copy -vcodec copy -map 2 -c:s:0 mov_text -metadata:s:s:0 language=eng "Session 10072 - Principles of spatial design (1080p).mp4"
# 6.删除临时文件
rm "Session - 10072 temp.mp4"
rm "Session - 10072 temp.aac"
rm "Session - 10072 temp.vtt"
rm "Session - 10072 temp.srt"
rm "TranslateSession - 10072 temp.srt"
rm "TranslateSession - 10072 temp.vtt"
