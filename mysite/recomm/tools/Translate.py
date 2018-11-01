#调用有道词典的web接口进行翻译
#coding: utf-8
import requests
import json
import os

def translate(word=None):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key={
    #'type':"AUTO",
    'from': "zh-CHS", # Translate from Chinese to English
    'to': "EN",
    'i':word,
    "doctype":"json",
    "version":"2.1",
    "keyfrom":"fanyi.web",
    "ue":"UTF-8",
    "action":"FY_BY_CLICKBUTTON",
    "typoResult":"true"
    }
    #key这个字典为发送给有道词典服务器的内容，里面的i就是我们需要翻译的内容。此处直接调用word变量。
    response = requests.post(url,data=key)
    return response

def get_result(li=None):
    result = json.loads(li.text)
    text = ''
    for i in range(len(result['translateResult'][0])):
        text = text + str(result['translateResult'][0][i]['tgt'])
    return text

def Translate(ori_text_filepath,translate_text_filepath):
        print('Translating...')
        try:
            ori_text = open(ori_text_filepath, encoding='utf-8')
        except FileNotFoundError:
            print("*******file not found***********")
        else:
            text = ''
            # 处理文本，删除换行，重要！
            for line in ori_text.readlines():
                line2 = line.strip('\n')
                text = text + line2

            k = int(len(text)/5000)
            result = ''
            for i in range(k):
                totranslate = text[i*5000:i*5000+5000]
                #totranslate = '这句话的意思是'
                mid_result = translate(totranslate)
                translation = get_result(mid_result)
                result = result + translation
            # 剩下的文本进行翻译
            totranslate = text[k*5000:len(text)]
            mid_result = translate(totranslate)
            translation = get_result(mid_result)
            result = result + translation
            with open(translate_text_filepath, "w", encoding='utf-8') as f:
                f.write(result)
            print('Translate OK.')


if __name__ == '__main__':
    Translate()