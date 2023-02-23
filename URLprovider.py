import requests,os,sys,getopt,argparse
from urllib.parse import urlparse, parse_qs,urlunparse,urlencode

parser=argparse.ArgumentParser(description='Get Path and Cookie')
parser.add_argument('-c', '--cookie', type=str, default='', help='type your cookie here, default null. \n Example: JSESSIONID=6fiCgX-Ju5XS0Pf85QbMcvUe9PUAfF1rnq7SJRTW')
parser.add_argument('-n', '--name', type=str, required=True, help= 'type the name of project. Example: webgoat')
parser.add_argument('-u', '--host', type=str, default='localhost', help='type your host here. \n Example: 192.168.1.1')
parser.add_argument('-p', '--port', type=str, default='8080', help='type your port here. \n Example: 8080')

args = parser.parse_args()
folder_path = './' + args.name
cookie = args.cookie
host = args.host
port = args.port
print(folder_path)
def get_url_params(url):
    parsed_url = urlparse(url)
    query_params = parsed_url.query
    return query_params
def remove_url_params(url):
    parsed_url = urlparse(url)
    # 创建一个新的解析结果，只保留原始URL的方案、网络位置和路径
    new_parsed_url = parsed_url._replace(query=None)
    # 将新的解析结果转换为字符串URL
    new_url = urlunparse(new_parsed_url)
    return new_url

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            # 对文件进行处理
            request_text = f.read()
            # 解析URL,将要请求的host添加到下面
            url = 'http://' + host + ':' + port + request_text.split()[1]
            # 解析请求头和请求体
            request_lines = request_text.strip().split("\n")
            request_headers = {}
            request_body = ""
           #解析headers和body
            for line in request_lines[2:15]:
                if ":" in line :
                    header, value = line.split(":", 1)
                    request_headers[header.strip()] = value.strip()
            for line in request_lines[10:]:
                request_body = line.strip()
            request_headers['Cookie']=cookie
            #判断方式并发送请求
            if 'GET' in request_text:
                params = get_url_params(url)
                new_url = remove_url_params(url)
                response = requests.get(new_url, headers=request_headers,params=params)
            elif 'POST' in request_text:
                response = requests.post(url, headers=request_headers, data=request_body)
            #回显
            print(response)




