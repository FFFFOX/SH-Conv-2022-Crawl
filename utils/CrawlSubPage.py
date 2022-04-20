from typing import Tuple
import requests
from lxml import html

addr_df = pd.DataFrame()
LAST = ['村','弄','号','园','区','宅','沿']

def getNormalPage(date, url, send_headers) -> Tuple:
    '''
    data: 键，可以是日期或是标题，主要是表明url对应的日期
    url: 子网页url
    send_headers: 伪装
    '''
    addr = []
    response = requests.get(url,headers=send_headers).text
    selector = html.fromstring(response)
    contents = selector.xpath("//div[@class='main-container margin-top-15']//div[@class='Article_content']/p")

    for content in contents:
        possibleLoc = content.xpath('span/span/text()')
        loc = content.xpath('span/text()')
        if loc != []:
            # print(loc[0][-1:] in last)
            if possibleLoc != []:
                loc[0] = possibleLoc[0]+loc[0]
        
            if loc[0][-1:] == '，' or loc[0][-1:] == '：':
                # loc = loc[0].replace(',',' ')
                addr.append(loc[0][:-1])
            elif loc[0][-1:] == '。' and loc[0][-1:] in LAST:
                addr.append(loc[0][:-1])
    return (date,addr)

def getWxPage(date, url, send_headers) -> Tuple:
    '''
    data: 键，可以是日期或是标题，主要是表明url对应的日期
    url: 子网页url
    send_headers: 伪装
    '''
    addr = []
    response = requests.get(url,headers=send_headers).text
    selector = html.fromstring(response)
    selector = html.fromstring(response)
    contents = selector.xpath("//div[@class='rich_media_inner']//div[@class='rich_media_area_primary_inner']//div[@class='rich_media_wrp']//div[@id='js_content']//section[@data-id='72469']//section[@data-autoskip='1']/p")

    for content in contents:
        loc = content.xpath('span/text()')
        if loc != []:
            # print(loc[0][-1:] in last)
            if loc[0][-1:] == '，' or loc[0][-1:] == '：':
                # loc = loc[0].replace(',',' ')
                addr.append(loc[0][:-1])
            elif loc[0][-1:] == '。' and loc[0][-1:] in last:
                addr.append(loc[0][:-1])
    return (date,addr)
