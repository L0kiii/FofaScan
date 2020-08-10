"""
@name: FOFA-HostDetails-Search
@another: L0ki
@time: 2020/08/07
@blog: https://l0ki.top
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import os
import time
import codecs
import json
import re
import requests
from requests.models import Response

header = {
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    'Cookie': "_fofapro_ars_session="+input("Cookie(not necessary):"),#请在此处填写cookie
    'Connection': "keep-alive"
}

url=input("识别Url:")
host = "https://fofa.so/hosts/" + url


def read_config():
    config_file = os.path.join("fofacms.json")
    with open(config_file, 'r',encoding='utf-8') as f:
        mark_list = json.load(f)
    return mark_list
 
 
class Fofacms:
 
    def __init__(self, html, title):
        self.html = html.lower()
        self.title = title.lower()
 
    def get_result(self, a):
        builts = ["(body)\s*=\s*\"", "(title)\s*=\s*\""]
        if a is True:
            return True
        if a is False:
            return False
        for regx in builts:
            match = re.search(regx, a, re.I | re.S | re.M)
            if match:
                name = match.group(1)
                length = len(match.group(0))
                content = a[length: -1]
                if name == "body":
                    if content.lower() in self.html:
                        return True
                    else:
                        return False
                elif name == "title":
                    if content.lower() in self.title:
                        return True
                    else:
                        return False
        raise Exception("不能识别的a:" + str(a))
 
    def calc_express(self, expr):
        #  title="NBX NetSet" || (header="Alternates" && body="NBX")
        #  1||(2&&3) => 1 2 3 && ||
        # header="X-Copyright: wspx" || header="X-Powered-By: ANSI C"
        # header="SS_MID" && header="squarespace.net"
        expr = self.in2post(expr)
        # print("后缀表达式", expr)
 
        stack = []
        special_sign = ["||", "&&"]
        if len(expr) > 1:
            for exp in expr:
                if exp not in special_sign:
                    stack.append(exp)
                else:
                    a = self.get_result(stack.pop())
                    b = self.get_result(stack.pop())
                    c = None
                    if exp == "||":
                        c = a or b
                    elif exp == "&&":
                        c = a and b
                    stack.append(c)
            if stack:
                return stack.pop()
        else:
            return self.get_result(expr[0])
 
    def in2post(self, expr):
        """ :param expr: 前缀表达式
            :return: 后缀表达式
 
            Example：
                1||(2&&3) => 1 2 3 && ||
        """
        stack = []  # 存储栈
        post = []  # 后缀表达式存储
        special_sign = ["&&", "||", "(", ")"]
        builts = ["body\s*=\s*\"", "title\s*=\s*\""]
 
        exprs = []
        tmp = ""
        in_quote = 0  # 0未发现 1发现 2 待验证状态
        for z in expr:
            is_continue = False
            tmp += z
            if in_quote == 0:
                for regx in builts:
                    if re.search(regx, tmp, re.I):
                        in_quote = 1
                        is_continue = True
                        break
            elif in_quote == 1:
                if z == "\"":
                    in_quote = 2
            if is_continue:
                continue
            for i in special_sign:
                if tmp.endswith(i):
 
                    if i == ")" and in_quote == 2:
                        # 查找是否有左括号
                        zuo = 0
                        you = 0
                        for q in exprs:
                            if q == "(":
                                zuo += 1
                            elif q == ")":
                                you += 1
                        if zuo - you < 1:
                            continue
                    # print(": " + tmp + " " + str(in_quote))
                    length = len(i)
                    _ = tmp[0:-length]
                    if in_quote == 2 or in_quote == 0:
                        if in_quote == 2 and not _.strip().endswith("\""):
                            continue
                        if _.strip() != "":
                            exprs.append(_.strip())
                        exprs.append(i)
                        tmp = ""
                        in_quote = 0
                        break
        if tmp != "":
            exprs.append(tmp)
        if not exprs:
            return [expr]
        # print("分离字符", exprs)
        for z in exprs:
            if z not in special_sign:  # 字符直接输出
                post.append(z)
            else:
                if z != ')' and (not stack or z == '(' or stack[-1] == '('):  # stack 不空；栈顶为（；优先级大于
                    stack.append(z)  # 运算符入栈
 
                elif z == ')':  # 右括号出栈
                    while True:
                        x = stack.pop()
                        if x != '(':
                            post.append(x)
                        else:
                            break
 
                else:  # 比较运算符优先级，看是否入栈出栈
                    while True:
                        if stack and stack[-1] != '(':
                            post.append(stack.pop())
                        else:
                            stack.append(z)
                            break
        while stack:  # 还未出栈的运算符，需要加到表达式末尾
            post.append(stack.pop())
        return post
 
 
def fingerprint(body):
    mark_list = read_config()
    # title
    m = re.search('<title>(.*?)<\/title>', resp, re.I | re.M | re.S)
    title = ""
    if m:
        title = m.group(1).strip()
    fofa = Fofacms(body, title)
    whatweb = ""
    for item in mark_list:
        express = item["rule"]
        name = item["name"]
        # print("rule:" + express)
        try:
            if fofa.calc_express(express):
                whatweb = name.lower()
                break
        except Exception:
            print("fofacms error express:{} name:{}".format(express, name))
    return whatweb

cms_url = "http://" + url
resp = requests.get(cms_url).text
def getData():
    global component, product, port
    ret = urllib.request.Request(url=host, headers=header)
    if ret: print("[+]Login Success...")
    else: print("[*]Login Failed ...")

    # 打开网页
    res = urllib.request.urlopen(ret)
    if res: print("[+]Open Success...")
    else: print("[*]Open Failed...")

    # 转化格式
    response = BeautifulSoup(res, 'html.parser')
    if response: print("[+]Change Success...")
    else: print("[*]Change Failed...")


    # 找到想要数据的父元素
    pattern_ip = re.compile(r'var ip = "(.*?)"')
    pattern_key = re.compile(r'var key = "(.*?)"', re.S)
    ip = pattern_ip.findall(str(response))
    key = pattern_key.findall(str(response))
    print("[+]This is ip:"+" "+ip[0])
    print("[+]This is key:"+" "+key[0])

    # 正则接口获取组件信息
    json_url = "https://fofa.so/ajax/get_rules?ip=" + ip[0] + "&key=" + key[0]
    print("[+]This is successful splicing Url:"+" "+json_url)
    # 处理请求数据
    json_response = requests.get(url=json_url, headers=header)
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
        cms=fingerprint(resp)
        for item in data:
            TCP_data = item.find('div', {'class': 'ip-table-item marBot10 padBot2'}).get_text().replace('\n\n', '').replace('\n', ' ')
            pattern_tcp=re.compile(r'.*? 协议（.*?）：.*?')
            TCP_change=pattern_tcp.findall(TCP_data)
            TCP=TCP_data.replace(TCP_change[0], ' ')

            dict1 = {
                'url':url,
                'ip': ip,
                '协议': TCP,
                '端口': port,
                '组件': product,
                'CMS':cms
            }
            try:
                with codecs.open(file_path, 'a', encoding="utf-8") as fp:
                    fp.write(json.dumps(dict1, ensure_ascii=False) + '\n')
                    if fp.write: print("[+]Save Success...")
            except IOError as err:
                print('[*]error' + str(err))
            finally:
                fp.close()
    pass


if __name__ == '__main__':
    print("""
                ______       __        _____                    
                |  ___|     / _|      /  ___|                   
                | |_  ___  | |_  __ _ \ `--.   ___  __ _  _ __  
                |  _|/ _ \ |  _|/ _` | `--. \ / __|/ _` || '_ \ 
                | | | (_) || | | (_| |/\__/ /| (__| (_| || | | |
                \_|  \___/ |_|  \__,_|\____/  \___|\__,_||_| |_|
                                                                
blog: https://l0ki.top
github: https://github.com/L0kiii/FofaScan
usage: python3 HostDetails.py                                                        
""")
    getData()
