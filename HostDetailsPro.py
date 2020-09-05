"""
@name: FOFA-HostDetails-Search
@author: L0ki
@time: 2020/08/07
@blog: https://l0ki.top
@usage: 无指纹识别批处理版
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import os
import time
import codecs
import json
import re
import requests
from urllib.request import ProxyHandler, build_opener

header = {
            'Host': 'fofa.so',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': "_fofapro_ars_session="+input("Cookie(not necessary):"),#请在此处填写cookie,
            'If-None-Match': 'W/"6be1d30e6fc62489613ccd8d98678f73"',
            'Connection': 'close'
        }
proxy={
"http":"http://127.0.0.1:1080"
}

proxy_handler = ProxyHandler({
'http': 'http://127.0.0.1:1080'
})
with open(file="urls.txt", mode="r", encoding="utf-8") as f:
    urls = f.readlines()
    for do in urls:
        url = do.strip("\n")
        host = "https://fofa.so/hosts/" + url
        global component, product, port
        opener = build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        ret = urllib.request.Request(url=host, headers=header)
        if ret:
            print("[+]Login Success...")
        else:
            print("[*]Login Failed ...")

        # 打开网页
        res = urllib.request.urlopen(ret)
        if res:
            print("[+]Open Success...")
        else:
            print("[*]Open Failed...")

        # 转化格式
        response = BeautifulSoup(res, 'html.parser')
        if response:
            print("[+]Change Success...")
        else:
            print("[*]Change Failed...")

        # 找到想要数据的父元素
        pattern_ip = re.compile(r'var ip = "(.*?)"')
        pattern_key = re.compile(r'var key = "(.*?)"', re.S)
        ip = pattern_ip.findall(str(response))
        key = pattern_key.findall(str(response))
        print("[+]This is ip:" + " " + ip[0])
        print("[+]This is key:" + " " + key[0])
        if ip[0] == '':
            continue
        else:
            # 正则接口获取组件信息
            json_url = "https://fofa.so/ajax/get_rules?ip=" + ip[0] + "&key=" + key[0]
            print("[+]This is successful splicing Url:" + " " + json_url)
            # 处理请求数据
            json_response = requests.get(url=json_url, headers=header,proxies=proxy)
            json_data = json_response.text
            component = json.loads(json_data)
            # 创建存放数据的文件夹
            folder_name = "output"
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # 定义文件
            current_time = time.strftime('%Y-%m-%d', time.localtime())
            file_name = "results" + current_time + ".json"

            # 文件路径
            file_path = folder_name + "/" + file_name

            # 端口
            # 组件
            # cms
            for i in component['rules']:
                port = i
                product = component['rules'][i]['data'][0]['product']
                data = response.find_all('body')
                for item in data:
                    TCP_data = item.find('div', {'class': 'ip-table-item marBot10 padBot2'}).get_text().replace('\n\n','').replace('\n', ' ')
                    pattern_tcp = re.compile(r'.*? 协议（.*?）：.*?')
                    TCP_change = pattern_tcp.findall(TCP_data)
                    TCP = TCP_data.replace(TCP_change[0], ' ')

                    dict1 = {
                        'url': url,
                        'ip': ip,
                        '协议': TCP,
                        '端口': port,
                        '组件': product
                    }
                    try:
                        with codecs.open(file_path, 'a', encoding="utf-8") as fp:
                            fp.write(json.dumps(dict1, ensure_ascii=False) + '\n')
                            if fp.write:
                                print("[+]Save Success...")
                    except IOError as err:
                        print('[*]error' + str(err))
                    finally:
                        fp.close()
            pass
