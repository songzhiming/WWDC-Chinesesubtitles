import openai
import pysrt
import backoff  # for exponential backoff
import fire

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def get_completion(prompt, model = "gpt-3.5-turbo"):
    openai.api_key = "sk-xxx"
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

def getSrt(srtPath, translateSrtPath):
    srt = pysrt.open(srtPath)
    for element in srt.data:
        text = element.text
        translateText = translate(text).replace("```","")
        element.text = text + "\n" + translateText
        print(f'原文, {text}')
        print(f'翻译后, {translateText}')
    srt.save(translateSrtPath)


if __name__ == '__main__':
    fire.Fire()
