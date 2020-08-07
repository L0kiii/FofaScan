## 【红队信息收集利器】FOFA Host Details

 IP 端口 协议 网站组件分层  指纹识别 序列化输出显示

指纹识别基于`@another:w8ay`

## 用法

```python
#若cms无对应值则代表识别不到
python3 HostDetails.py
```

## 组件信息

![image-20200807143505847](https://l0ki-town.oss-cn-beijing.aliyuncs.com/l0ki.top/image-20200807143505847.png)



## 组件分层

![image-20200807143425425](https://l0ki-town.oss-cn-beijing.aliyuncs.com/l0ki.top/image-20200807143425425.png)

## 爬取结果

```json
{"url": "baidu.com", "ip": ["39.156.69.79"], "协议": " https http", "端口": "443", "组件": "D***********t","CMS":""}
{"url": "baidu.com", "ip": ["39.156.69.79"], "协议": " https http", "端口": "80", "组件": "Apache-Web-Server","CMS":""}
....

if u r vip:
{"url":"baidu.com","ip": ["39.156.69.79"], "协议": " https http", "端口": "443", "组件": "DigiCert-Cert","CMS":""}
{"url":"baidu.com","ip": ["39.156.69.79"], "协议": " https http", "端口": "80", "组件": "Apache-Web-Server","CMS":""}
....
```

