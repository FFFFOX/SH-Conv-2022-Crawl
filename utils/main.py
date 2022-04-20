import requests
from lxml import html
import time
import collections
import pandas as pd
from openpyxl import load_workbook
from CrawlSubPage import *

send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}

target_html_dict = collections.OrderedDict()
BASE_URL = 'https://wsjkw.sh.gov.cn'
for i in range(1,16):
    time.sleep(1)
    page = '_'+str(i)
    if i == 1:
        page = ''
    url = 'https://wsjkw.sh.gov.cn/xwfb/index{}.html'.format(page)
    response = requests.get(url,headers=send_headers).text
    # print(response)
    selector = html.fromstring(response)
    urls = selector.xpath("//div[@class='main-container margin-top-15']//ul[@class='uli16 nowrapli list-date ']/li")
    for url in urls:
        title = url.xpath('a/@title')[0]
        herf = url.xpath('a/@href')[0]
        if '（0-24时）' in title:
            print(title)  
            # print(BASE_URL + herf)
            if herf[:4] == 'http':
                target_html_dict[title] = herf
            else:
                target_html_dict[title] = BASE_URL + herf
# for url in target_html_dict.items():
#     print(url)


wb = load_workbook('./data.xlsx')
excel_writer = pd.ExcelWriter('data.xlsx',engine='openpyxl')
# print(excel_writer.path)
excel_writer.book = wb

for title,url in target_html_dict.items():
    # print(url[8:17])
    if url[8:17] == 'mp.weixin':
    # if url == 'https://mp.weixin.qq.com/s/vxFiV2HeSvByINUlTmFKZA':
        res = getWxPage(date=title,url=url)
    # elif url == 'https://wsjkw.sh.gov.cn/xwfb/20220321/2cda1b24b5304d118352bdfd32af0aa4.html':
    else:
        res = getNormalPage(date=title,url=url)
    
    _t_df = pd.DataFrame()
    _t_df['地址'] = res[1]
    _t_df.to_excel(excel_writer, sheet_name=res[0],)

excel_writer.save() # 储存文件 
excel_writer.close() 
