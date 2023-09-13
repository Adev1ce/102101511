import requests
import re
import warnings
import json
import jieba
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from collections import Counter

cnt = 1
headers = {
    'cookie': 'buvid3=D33649ED-6F6C-FB48-650D-DBD271B5798C10363infoc; b_nut=1667930410; i-wanna-go-back'
              '=-1; _uuid=E6D2C6DB-D7C10-2C37-C8DF-4'
              '32105D1F4E1C10779infoc; nostalgia_conf=-1; fingerprint=85a0718862c972e5c43ea89d79f'
              '89c01; buvid_fp_plain=undefined; DedeUser'
              'ID=35348020; DedeUserID__ckMd5=d4925eeb9f0b12dc; buvid_fp=85a0718862c972e5c43ea89'
              'd79f89c01; b_ut=5; rpdid=|(u)luk)~Rmm0J\'uYY)~RYmRm; he'
              'ader_theme_version=CLOSE; LIVE_BUVID=AUTO7416771612534930; PVID=1; hit-new-styl'
              'e-dyn=0; hit-dyn-v2=1; CURRENT_PID=f2d2be40-d80f-11ed-8621-ed4'
              'dcf5719e2; buvid4=8514995C-AB15-02D2-859B-28D1CA8BAEBE13673-022110902-vdG'
              'T0WAv%2FuLSZMFqZv9vXg%3D%3D; FEED_LIVE_VERSION=V8; CURRENT_FNVAL=40'
              '48; CURRENT_QUALITY=116; b_lsid=3E39F69B_18A6A83AD92; SESSDATA=d1784012'
              '%2C1709556129%2C43b20%2A91; bili_jct=059718cf8b145b09692ac96f7972e358; bili_t'
              'icket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE'
              '2OTQyNjMzMzQsImlhdCI6MTY5NDAwNDEzNCwicGx0IjotMX0.9yROhIoiStJYWxbl2fbcMYFfQSX'
              '1nAatFa1wZ3xR-Is; bili_ticket_expires=1694263334; sid=5p46w4bf; bp_vid'
              'eo_offset_35348020=838228533586165810; home_feed_column=5; browser_resolution=1865-969',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KH'
                  'TML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/116.0.1938.69'
}
# 获取弹幕地址


def get_danmu_url(video_str):
    url = video_str
    response = requests.get(url=url, headers=headers)
    html = response.text
    cid = re.search('"cid":(.*?),', html).groups()[0]
    danmu_url = f'https://comment.bilibili.com/{cid}.xml'
    return danmu_url

# 获取视频地址


def get_vedio(bv):
    vedio_url = "https://www.bilibili.com/video/"+bv
    return vedio_url
# 获取bv号


def get_bvid(url, pos):

    # 通过搜索api“https://api.bilibili.com/x/web-interface/search/all/v2?page=1-15&keyword=”获取前300个视频的bvid
    res = requests.get(url=url, headers=headers).text
    json_dict = json.loads(res)
    return json_dict["data"]["result"][11]["data"][pos]["bvid"]

# 统计弹幕次数


def count_danmu():
    # 打开TXT文件以读取数据
    file_path = '弹幕.txt'

    # 初始化一个空的文本字符串，用于累积所有文本数据
    danmu_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 在这里处理每一行的数据
            # 示例：将每一行的弹幕添加到danmu_list列表中
            danmu_list.append(line.strip())

    # 使用Counter统计弹幕出现次数
    danmu_counter = Counter(danmu_list)
    # 获取出现次数排名前20的弹幕
    top_20_danmus = danmu_counter.most_common(20)

    # 打印排名前20的弹幕及其出现次数
    for idx, (danmu, count) in enumerate(top_20_danmus, 1):
        print(f'排名 #{idx}: 弹幕 "{danmu}" 出现次数：{count}')
    top_76016_danmus = danmu_counter.most_common(76016)
    df = pd.DataFrame(top_76016_danmus, columns=['弹幕', '次数'])
    df.to_excel('统计弹幕次数.xlsx', index=False)

# 生成云图


def make_graph():
    text_data = ''
    with open('弹幕.txt', 'r', encoding='utf-8') as file:
        for line in file:
            text_data += line.strip() + ' '

    # 使用jieba进行中文分词
    words = jieba.cut(text_data, cut_all=False)
    word_list = " ".join(words)

    # 加载自定义形状图片
    shape_mask = np.array(Image.open('img.png'))

    # 创建词云图对象，并设置形状
    wordcloud = WordCloud(width=1000,
                          background_color='white',
                          mask=shape_mask,  # 使用自定义形状
                          contour_width=1,
                          contour_color='white',  # 边框颜色
                          font_path='STKAITI.TTF',  # 用于中文显示的字体文件
                          max_words=300000,  # 最多显示的词语数量
                          colormap='Blues',  # 颜色映射，可以根据需要更改
                          ).generate(word_list)

    # 使用形状图片的颜色
    image_colors = ImageColorGenerator(shape_mask)
    wordcloud.recolor(color_func=image_colors)

    # 显示词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 隐藏坐标轴
    plt.title('')
    plt.show()


def main():
    # warnings.filterwarnings("ignore")
    global cnt
    for i in range(15):
        url = f'https://api.bilibili.com/x/web-interface/search/all/v2?page={i}&keyword=日本核污染水排海'
        for j in range(20):
            print(cnt)
            cnt += 1
            bv = get_bvid(url, j)
            vedio_url_data = get_vedio(bv)
            danmu_url = get_danmu_url(vedio_url_data)
        # print(danmu_url)
            response = requests.get(url=danmu_url, headers=headers)
            response.encoding = response.apparent_encoding
            pattern = '<d p=".*?">(.*?)</d>'
            datalist = re.findall(pattern, response.text)
        # print(DataList)
            f = open('弹幕.txt', mode='a', encoding='utf-8')
            for k in range(len(datalist)):
                f.write(datalist[k]+'\n')
            f.close()
    warnings.filterwarnings("ignore")
    count_danmu()
    make_graph()


if __name__ == '__main__':
    main()
