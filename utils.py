# -*-coding:utf8-*-
import re
import requests
import time
from bs4 import BeautifulSoup
# import datetime


def get_html(url, headers=None, data=None):
    return requests.post(url, headers=headers, data=data).content


def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))
    return current_milli_time()


def timestamp_to_datetime(d):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d))

# print int(round(time.time() * 1000))
# print datetime_to_timestamp_in_milliseconds(datetime.datetime.now())


# def get_cids(aid):
#     cids = []
#     av_url = 'http://www.bilibili.com/video/av'+str(aid)+'/'
#     pattern1 = re.compile(r'/video/av.*/(index_.*).html')
#     pattern2 = re.compile(r'cid=(\d{5,10})&aid=(\d{5,10})&pre')
#     av_content = get_html(av_url)
#     indexes = pattern1.findall(av_content)
#     if not len(indexes):  # not == []
#         cids[0] = pattern2.search(av_content).group(1)
#     else:
#         for index in indexes:
#             cid_url = 'http://www.bilibili.com/video/av'+str(aid)+'/'+index+'.html'
#             cid_content = get_html(cid_url)
#             cid = pattern2.search(cid_content).group(1)
#             cids.append(cid)
#     return cids


def parse_danmu(cid):
    danmu_url = 'http://comment.bilibili.com/' + str(cid) + '.xml'
    xml = get_html(danmu_url)
    soup = BeautifulSoup(xml)
    elems = soup.find_all('d')
    # use elem['p'] elem.text
    return elems
