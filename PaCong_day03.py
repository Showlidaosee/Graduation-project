# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 09:57:06 2019

@author: chensiyi
"""

import os
import requests
from lxml import etree
import pandas as pd

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
cookies = {'SUB': 'SECKEY_ABVK=G0NOubs+G1nd4GaVk1B3pk/C1l39FynwIcmNyMVK9hI%3D; '
                  'BMAP_SECKEY=Qk_XaCnqY4Pk3xPt73kG36fnqwwTbqw39FxSp9pzdMPMRSH9DCRFzQ'
                  'eaxsFKMO2X0TKd17xnVOjoUZSQja_S5pYgupzA-19Qg5mC_RHcy9ilaTQ3SkCZJrwOyxC0L'
                  '46Y-3wVPAZUvpzGzeC4A6uaNlu5XVZLRCGkG1wQlIoCEOfQTMp3KLTSq8fnIGlRUys; route=65389440'
                  'feb63b53ee0576493abca26d; Hm_lvt_82932fc4fc199c08b9a83c4c9d02af11=1649211467,1649236158;'
                  ' Hm_lpvt_82932fc4fc199c08b9a83c4c9d02af11=1649236158; SECKEY_ABVK=G0NOubs+G1nd4GaVk1B3pgEpF'
                  'CxBxNYOClDwCeOq5T8%3D; BMAP_SECKEY=Qk_XaCnqY4Pk3xPt73kG36pvEjWNUGgz5A1jAJXlfKXuzooPaG-0nHvFrlM'
                  'w78voHLv0IqFeLpUcmSb6ukszfy3ggQeq0jiqZNZhIXzYMbx6kdku1C2o0-g6jqt6Ry6tEe6h8L8yf01uaXLT10Oz2UQNkQ_'
                  'vVGaQXdz8MH4ubek2alqG6ouxTu1Z8hprY6YB'}


def get_data(url):
    r = requests.get(url, headers=headers, cookies=cookies, timeout=30)
    r.raise_for_status()  # 查看是否正常，正常返回200,否则返回404等
    r.encoding = 'utf-8'
    return r.text


local_data = 'D:/D_showlidaosee'
local_main2 = local_data + '/' + 'movie.csv'  # 设置路径
if not os.path.exists(local_main2):
    data = pd.DataFrame(columns=['电影名称', '电影详情页', '电影类型', '电影票房', '国家及地区', '上映时间'])
    data.to_csv(local_main2, index=None, encoding="utf_8_sig")

urls = []
for year in range(5):
    urls.append('https://ys.endata.cn/BoxOffice/Ranking')

for url in urls:
    data = get_data(url)
    selector = etree.HTML(data)

    url = selector.xpath('//td[@class="one"]/a/@href')  # 详情页url
    name = selector.xpath('//td[@class="one"]/a/@title')  # 电影名称
    movie_type = selector.xpath('//*[@id="tbContent"]//tr//td[2]/text()')  # 电影类型
    box_office = selector.xpath('//*[@id ="tbContent"]//tr//td[3]/text()')  # 电影票房
    country = selector.xpath('//*[@id="tbContent"]//tr//td[6]/text()')  # 国家及地区
    time = selector.xpath('//*[@id="tbContent"]//tr//td[7]/text()')  # 上映时间

    for i in range(len(url)):
        data = pd.DataFrame({'电影名称': name[i],
                             '电影详情页': url[i],
                             '电影类型': movie_type[i],
                             '电影票房': box_office[i],
                             '国家及地区': country[i],
                             '上映时间': time[i]},
                            columns=['电影名称', '电影详情页', '电影类型', '电影票房', '国家及地区', '上映时间'], index=[0])
        data.to_csv(local_main2, index=None, mode='a', header=None, sep=',', encoding="utf_8_sig")


