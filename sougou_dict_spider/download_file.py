# coding = utf-8

import requests
from lxml.html import fromstring
import os
from urllib.parse import urljoin

scel_dir = 'scel_dicts'
base_url = "https://pinyin.sogou.com/dict/"
res = requests.get(base_url)
text = res.text
res.close()
body = fromstring(text)
catewords_urls = dict(zip(body.xpath('//div[@class="catewords"]/a[@href]/text()') ,
                          body.xpath('//div[@class="catewords"]/a/@href')))

def get_download_url(cateword, cateurl):
    cateurl = urljoin(base_url, cateurl)
    cate_dir = os.path.join(scel_dir, cateword)
    if not os.path.exists(cate_dir):
        os.makedirs(cate_dir)
    res = requests.get(cateurl)
    body = fromstring(res.text)
    for file_name, url in zip(body.xpath('//div[@class="detail_title"]/a/text()'),
                              body.xpath('//div[@class="dict_dl_btn"]/a/@href')):
        file_name = file_name.strip().replace(' ','').replace('/', '').replace('.','').replace('\\','')
        file_path = os.path.join(cate_dir, file_name + '.scel')
        download_file(url, file_path)
        print(f'success download file into {file_path}')
    cateurl_pages = body.xpath('//div[@id="dict_page_list"]//li//a/text()')
    if cateurl_pages[-1] == '下一页':
        cateurl = body.xpath('//div[@id="dict_page_list"]//li//a/@href')[-1]
        get_download_url(cateword, cateurl)

def download_file(url, filepath):
    res = requests.get(url)
    with open(filepath, 'wb') as fp:
        fp.write(res.content)

if __name__ == '__main__':
    for cateword, cateurl in catewords_urls.items():
        get_download_url(cateword, cateurl)
