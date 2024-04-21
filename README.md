```markdown
## 【Red Team Information Gathering Tool】FOFA Host Details

`Author: L0ki`

`Blog: [https://l0ki.top](https://l0ki.top)`

`Acknowledgements: l3yx`

IP Port Protocol Website Component Layer Fingerprinting CMS Serialization Output Display

Fingerprinting based on `@author:w8ay`

## Usage

```python
# If there is no corresponding value for CMS, it means it cannot be identified
python3 HostDetails.py
```

## Component Information

![Image](https://l0ki-town.oss-cn-beijing.aliyuncs.com/l0ki.top/image-20200807143505847.png)

## Component Layering

![Image](https://l0ki-town.oss-cn-beijing.aliyuncs.com/l0ki.top/image-20200807143425425.png)

## Crawling Results

```json
{"url": "baidu.com", "ip": ["39.156.69.79"], "Protocol": "https http", "Port": "443", "Component": "D***t", "CMS": ""}
{"url": "baidu.com", "ip": ["39.156.69.79"], "Protocol": "https http", "Port": "80", "Component": "Apache-Web-Server", "CMS": ""}
....

If you are a VIP:
{"url": "baidu.com", "ip": ["39.156.69.79"], "Protocol": "https http", "Port": "443", "Component": "DigiCert-Cert", "CMS": ""}
{"url": "baidu.com", "ip": ["39.156.69.79"], "Protocol": "https http", "Port": "80", "Component": "Apache-Web-Server", "CMS": ""}
....
```
```
